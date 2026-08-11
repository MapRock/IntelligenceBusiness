"""Trace outer query items and filters through CTEs/subqueries to base columns.

This module preserves the October 2025 stepwise lineage algorithm while
removing its hard-coded command-line file path. It requires the optional
``sqlglot`` dependency.
"""

from sqlglot import parse_one, exp
from typing import Dict, Tuple, Any, List, Optional, Iterable
from pathlib import Path

# ---------------- core helpers ----------------
def qname(t: exp.Table) -> str:
    db = t.args.get("db")
    nm = t.name
    return f"{db}.{nm}" if db else nm

def outer_select(root: exp.Expression) -> exp.Select:
    if isinstance(root, exp.Select): return root
    if isinstance(root, exp.With):   return outer_select(root.this)
    if hasattr(root, "this") and isinstance(root.this, exp.Select): return root.this
    return root.find(exp.Select) or root

def build_cte_definitions(root: exp.Expression) -> Dict[str, exp.Select]:
    ctes = {}
    with_ = root.find(exp.With)
    if not with_:
        return ctes
    for c in with_.expressions:
        nm = c.alias_or_name
        body = c.this
        if isinstance(body, exp.Subquery):
            body = body.this
        ctes[nm] = body
    return ctes

def projection_map(sel: exp.Select) -> Dict[str, exp.Expression]:
    out = {}
    for it in sel.expressions:
        if isinstance(it, exp.Alias) and it.alias:
            out[it.alias] = it.this
        elif isinstance(it, exp.Column):
            out[it.name] = it
        else:
            # expression without alias (referenceable only by SQL text)
            out[it.sql(dialect="tsql")] = it
    return out

def proj_lookup(name: str, mp: Dict[str, exp.Expression]) -> Optional[exp.Expression]:
    if name in mp:
        return mp[name]
    low = name.lower()
    for k, v in mp.items():
        if k.lower() == low:
            return v
    return None

def alias_of(node) -> Optional[str]:
    a = getattr(node, "alias", None) or node.args.get("alias")
    if isinstance(a, exp.TableAlias):
        return a.name
    if isinstance(a, str):
        return a
    return None

def object_name(node) -> Optional[str]:
    return getattr(node, "alias_or_name", None) or getattr(node, "name", None)

def scope_map_for_select(sel: exp.Select, cte_defs: Dict[str, exp.Select]) -> Dict[str, Tuple[str, Any]]:
    """
    Build a reliable scope map from ALL Table/Subquery sources in this SELECT.
    Keys registered:
      - alias
      - raw table/cte name
      - schema.table
    Values:
      ("table", "schema.table") or ("cte", <Select>)
    """
    amap: Dict[str, Tuple[str, Any]] = {}

    def register(key: Optional[str], obj):
        if not key:
            return
        o = obj
        if isinstance(o, exp.Subquery):
            o = o.this
        if isinstance(o, exp.Select):
            amap[key] = ("cte", o)
            return
        if isinstance(o, exp.Table):
            # CTE name used as a table?
            if o.name in cte_defs:
                body = cte_defs[o.name]
                amap[key] = ("cte", body)
                amap[o.name] = ("cte", body)
                return
            real = qname(o)
            amap[key] = ("table", real)
            amap[o.name] = ("table", real)
            amap[real] = ("table", real)
            return
        inner = o.find(exp.Table)
        if inner:
            register(key, inner)

    # All tables encountered
    for t in sel.find_all(exp.Table):
        a = alias_of(t)
        if a: register(a, t)
        register(t.name, t)
        register(qname(t), t)

    # FROM subqueries/aliases
    frm = sel.args.get("from")
    if frm:
        for src in frm.expressions:
            target = src.this if isinstance(src, exp.Alias) else src
            a = alias_of(src)
            if a and isinstance(target, (exp.Select, exp.Subquery)):
                register(a, target)
            nm = object_name(target)
            if nm:
                register(nm, target)

    # JOIN subqueries/aliases
    for j in sel.find_all(exp.Join):
        t = j.this
        target = t.this if isinstance(t, exp.Alias) else t
        a = alias_of(t)
        if a and isinstance(target, (exp.Select, exp.Subquery)):
            register(a, target)
        nm = object_name(target)
        if nm:
            register(nm, target)

    return amap

# function-like nodes (version tolerant)
_FN_NAMES = [
    "Func","Anonymous","Coalesce","Cast","DateFromParts","Extract","Trim",
    "Substring","DateTrunc","If","Case","Greatest","Least","Array","Tuple","Paren"
]
_FN_TYPES = tuple(getattr(exp, n) for n in _FN_NAMES if hasattr(exp, n))

def func_args(e: exp.Expression) -> Iterable[exp.Expression]:
    # common holders
    if hasattr(e, "expressions") and isinstance(e.expressions, list) and e.expressions:
        for x in e.expressions:
            yield x
    exps = e.args.get("expressions")
    if isinstance(exps, list):
        for x in exps:
            yield x

# ---------------- stepwise chain resolution ----------------
def column_display(col: exp.Column) -> str:
    return f"{col.table}.{col.name}" if col.table else col.name

def stepwise_chains_for_column(col: exp.Column,
                               scope: Dict[str, Tuple[str, Any]],
                               cte_defs: Dict[str, exp.Select]) -> List[List[str]]:
    """
    Return ALL possible stepwise chains for a Column reference:
      e.g.,  b.SalesAmount -> Base.SalesAmount -> dbo.FactInternetSales.SalesAmount
    """
    start = column_display(col)

    # CASE 1: qualified with alias or name that maps
    if col.table and col.table in scope:
        kind, target = scope[col.table]
        if kind == "table":
            # reached base table; terminal
            return [[start, f"{target}.{col.name}"]]
        if kind == "cte" and isinstance(target, exp.Select):
            # resolve against CTE projection
            pmap = projection_map(target)
            proj = proj_lookup(col.name, pmap)
            inner_scope = scope_map_for_select(target, cte_defs)
            if proj is not None:
                # next step name is CTE.OutputColumn
                next_step = f"{object_name(target) or '<CTE>'}.{col.name}"
                # expand deeper
                chains = chains_for_expr(proj, inner_scope, cte_defs)
                # prepend steps
                out = []
                for ch in chains:
                    out.append([start, next_step] + ch)
                # if projection goes directly to base table column, chains_for_expr returns [[real]]
                if not chains:
                    out.append([start, next_step])
                return out
            # fallback: if not in map, try columns with same name within CTE body
            hits = []
            for c in target.find_all(exp.Column):
                if c.name.lower() == col.name.lower():
                    subchains = stepwise_chains_for_column(c, inner_scope, cte_defs)
                    for sc in subchains:
                        hits.append([start, f"{object_name(target) or '<CTE>'}.{col.name}"] + sc[1:])  # keep continuity
            if hits:
                return hits
            # unknown projection — stop at CTE step
            return [[start, f"{object_name(target) or '<CTE>'}.{col.name}"]]

    # CASE 2: qualified but not known — best effort single step
    if col.table:
        return [[start, f"{col.table}.{col.name}"]]

    # CASE 3: unqualified — try all CTEs in scope that project this column name
    results: List[List[str]] = []
    for key, (kind, target) in scope.items():
        if kind == "cte" and isinstance(target, exp.Select):
            pmap = projection_map(target)
            proj = proj_lookup(col.name, pmap)
            if proj is not None:
                inner_scope = scope_map_for_select(target, cte_defs)
                next_step = f"{object_name(target) or key}.{col.name}"
                chains = chains_for_expr(proj, inner_scope, cte_defs)
                if chains:
                    for ch in chains:
                        results.append([start, next_step] + ch)
                else:
                    results.append([start, next_step])
    if results:
        return results

    # Final fallback: if exactly one real table in scope, attach it
    real_tables = [r for _, (k, r) in scope.items() if k == "table"]
    if len(set(real_tables)) == 1:
        return [[start, f"{real_tables[0]}.{col.name}"]]

    # Unknown
    return [[start]]

def chains_for_expr(expr: exp.Expression,
                    scope: Dict[str, Tuple[str, Any]],
                    cte_defs: Dict[str, exp.Select]) -> List[List[str]]:
    """
    Expand an arbitrary expression into one or more chains.
    - Column → stepwise column chains
    - Alias → chains of aliased expression (skip alias name in chain)
    - Window/Function → union of chains of child args
    - Other → nested columns under it
    """
    if isinstance(expr, exp.Column):
        return stepwise_chains_for_column(expr, scope, cte_defs)
    if isinstance(expr, exp.Alias):
        return chains_for_expr(expr.this, scope, cte_defs)
    if isinstance(expr, exp.Window):
        chains: List[List[str]] = []
        if expr.this:
            chains += chains_for_expr(expr.this, scope, cte_defs)
        # partition/order inputs
        part = expr.args.get("partition_by")
        if part and hasattr(part, "expressions"):
            for p in part.expressions:
                chains += chains_for_expr(p, scope, cte_defs)
        order = expr.args.get("order")
        if order and hasattr(order, "expressions"):
            for o in order.expressions:
                base = o.this if isinstance(o, exp.Ordered) else o
                chains += chains_for_expr(base, scope, cte_defs)
        for a in func_args(expr):
            chains += chains_for_expr(a, scope, cte_defs)
        return chains
    if isinstance(expr, _FN_TYPES):
        chains: List[List[str]] = []
        if hasattr(expr, "this") and isinstance(expr.this, exp.Expression):
            chains += chains_for_expr(expr.this, scope, cte_defs)
        for a in func_args(expr):
            chains += chains_for_expr(a, scope, cte_defs)
        # If no args yield chains, scan nested columns as last resort
        if not chains:
            for c in expr.find_all(exp.Column):
                chains += stepwise_chains_for_column(c, scope, cte_defs)
        return chains

    # Fallback: scan nested columns
    chains: List[List[str]] = []
    for c in expr.find_all(exp.Column):
        chains += stepwise_chains_for_column(c, scope, cte_defs)
    return chains

# ---------------- roles & extraction ----------------
def is_metric(expr: exp.Expression) -> Tuple[bool, Optional[str], Optional[exp.Expression]]:
    # Windowed aggregate
    if isinstance(expr, exp.Alias) and isinstance(expr.this, exp.Window):
        fn = expr.this.this
        if isinstance(fn, exp.AggFunc):
            label = fn.sql_name().upper()
            if getattr(fn, "args", {}).get("distinct") or getattr(fn, "distinct", False):
                label = f"{label}(DISTINCT)"
            payload = fn.this or (fn.expressions[0] if getattr(fn, "expressions", None) else None)
            return True, f"{label} OVER", payload
        inner = expr.this.find(exp.AggFunc)
        if inner:
            label = inner.sql_name().upper()
            if getattr(inner, "args", {}).get("distinct") or getattr(inner, "distinct", False):
                label = f"{label}(DISTINCT)"
            payload = inner.this or (inner.expressions[0] if getattr(inner, "expressions", None) else None)
            return True, f"{label} OVER", payload
        return False, None, None

    node = expr.this if isinstance(expr, exp.Alias) else expr
    if isinstance(node, exp.AggFunc):
        label = node.sql_name().upper()
        if getattr(node, "args", {}).get("distinct") or getattr(node, "distinct", False):
            label = f"{label}(DISTINCT)"
        payload = node.this or (node.expressions[0] if getattr(node, "expressions", None) else None)
        return True, label, payload

    return False, None, None

def group_exprs(sel: exp.Select) -> List[exp.Expression]:
    g = sel.args.get("group")
    return list(g.expressions) if g else []

def out_name(expr: exp.Expression) -> str:
    if isinstance(expr, exp.Alias) and expr.alias: return expr.alias
    if isinstance(expr, exp.Column):              return expr.name
    return expr.sql(dialect="tsql")

def unqualified_name(expr: exp.Expression) -> Optional[str]:
    if isinstance(expr, exp.Alias) and expr.alias: return expr.alias.lower()
    if isinstance(expr, exp.Column):               return expr.name.lower()
    return None

def match_group(sel_item: exp.Expression, grp_item: exp.Expression) -> bool:
    try:
        if sel_item == grp_item: return True
        if hasattr(sel_item, "sql") and hasattr(grp_item, "sql"):
            if sel_item.sql(dialect="tsql") == grp_item.sql(dialect="tsql"): return True
    except Exception:
        pass
    si, gi = unqualified_name(sel_item), unqualified_name(grp_item)
    if si and gi and si == gi: return True
    return gi == out_name(sel_item).lower() if gi else False

# ---------------- main API ----------------
def analyze_sql_stepwise(sql: str, sql_dialect: str = "tsql") -> List[Tuple[str, str, str]]:
    root = parse_one(sql, read=sql_dialect)
    cte_defs = build_cte_definitions(root)
    sel = outer_select(root)
    outer_scope = scope_map_for_select(sel, cte_defs)

    rows = []

    # Outer SELECT: dice & metrics
    gexpr = group_exprs(sel)
    for item in sel.expressions:
        role = "Metric" if is_metric(item)[0] else ("Dice" if any(match_group(item.this if isinstance(item, exp.Alias) else item, g) for g in gexpr) else "Select")
        name = out_name(item)
        chains = chains_for_expr(item, outer_scope, cte_defs)
        # Only keep unique printable chains (joined by ' -> ')
        seen = set()
        linear = []
        for ch in chains:
            # flatten chains-for-expr returns nested; ensure terminal step(s) included
            if not ch:
                continue
            s = " -> ".join(ch)
            if s not in seen:
                seen.add(s)
                linear.append(s)
        if not linear:
            # try nested columns if expr had no columns
            for c in item.find_all(exp.Column):
                for ch in stepwise_chains_for_column(c, outer_scope, cte_defs):
                    s = " -> ".join(ch)
                    if s not in seen:
                        seen.add(s)
                        linear.append(s)
        for s in linear:
            rows.append((role, name, s))

    # WHERE/HAVING across all scopes
    for s in root.find_all(exp.Select):
        scope = scope_map_for_select(s, cte_defs)
        wh = s.args.get("where")
        if wh:
            for c in wh.find_all(exp.Column):
                for ch in stepwise_chains_for_column(c, scope, cte_defs):
                    rows.append(("Filter", c.name, " -> ".join(ch)))
        hv = s.args.get("having")
        if hv:
            for c in hv.find_all(exp.Column):
                for ch in stepwise_chains_for_column(c, scope, cte_defs):
                    rows.append(("Filter", c.name, " -> ".join(ch)))

    # Stable order
    prio = {"Dice":0, "Filter":1, "Metric":2, "Select":3}
    rows.sort(key=lambda r:(prio.get(r[0],9), r[1].lower(), r[2].lower()))
    return rows
