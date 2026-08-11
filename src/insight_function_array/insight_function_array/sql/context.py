"""Extract QueryDef-oriented SQL column and clause metadata using sqlglot."""

from __future__ import annotations

from dataclasses import dataclass
import re

try:
    import sqlglot
    from sqlglot import exp
except ImportError as exc:  # delayed optional dependency error
    sqlglot = None
    exp = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

AGGREGATE_NAMES = {
    "SUM", "AVG", "MIN", "MAX", "COUNT", "STDDEV", "STDDEV_SAMP", "VAR", "VARIANCE"
}
FUNCTION_HEAD = re.compile(r"^\s*([A-Z_][A-Z0-9_]*)\s*\(", re.IGNORECASE)


@dataclass(frozen=True)
class ColumnReference:
    table: str
    column: str
    clause: str
    function: str | None
    is_aggregate: bool


@dataclass(frozen=True)
class OutputColumn:
    output_name: str
    expression_sql: str
    sources: tuple[tuple[str, str], ...]


def _require_sqlglot() -> None:
    if sqlglot is None:
        raise RuntimeError("SQL parsing requires the optional 'sqlglot' dependency.") from _IMPORT_ERROR


def parse_sql(sql: str, dialect: str = "tsql"):
    _require_sqlglot()
    try:
        return sqlglot.parse_one(sql.lstrip("\ufeff"), read=dialect)
    except Exception:
        return sqlglot.parse_one(sql.lstrip("\ufeff"), read="ansi")


def qualified_table_name(table) -> str:
    parts = [getattr(table, "catalog", None), getattr(table, "db", None), table.name]
    return ".".join(part for part in parts if part)


def build_alias_map(tree) -> dict[str, str]:
    alias_map = {}
    for table in tree.find_all(exp.Table):
        base = qualified_table_name(table) or table.name
        if table.alias:
            alias_map[table.alias] = base
        alias_map.setdefault(table.name, base)
    return alias_map


def clause_of(node) -> str:
    parent = node
    while parent is not None:
        if isinstance(parent, exp.Where):
            return "WHERE"
        if isinstance(parent, exp.Having):
            return "HAVING"
        if isinstance(parent, exp.Group):
            return "GROUP BY"
        if isinstance(parent, exp.Order):
            return "ORDER BY"
        if isinstance(parent, exp.Join):
            return "JOIN ON"
        if isinstance(parent, exp.Window):
            return "WINDOW"
        if isinstance(parent, exp.Select):
            return "SELECT"
        parent = parent.parent
    return "UNKNOWN"


def _function_name(node) -> str | None:
    name = getattr(node, "name", None)
    if isinstance(name, str) and name:
        return name.upper()
    key = getattr(node, "key", None)
    if isinstance(key, str) and key:
        return key.upper()
    try:
        text = node.sql(dialect="tsql")
    except Exception:
        text = ""
    match = FUNCTION_HEAD.match(text)
    return match.group(1).upper() if match else None


def function_context_for_column(column) -> tuple[str | None, bool, list[str]]:
    names = []
    aggregate = None
    parent = column.parent
    while parent is not None and not isinstance(parent, exp.Select):
        name = _function_name(parent)
        if name:
            names.append(name)
            if name in AGGREGATE_NAMES and aggregate is None:
                aggregate = name
        parent = parent.parent
    primary = aggregate or (names[0] if names else None)
    return primary, aggregate is not None, names


def extract_column_references(sql: str, dialect: str = "tsql") -> list[ColumnReference]:
    tree = parse_sql(sql, dialect)
    alias_map = build_alias_map(tree)
    seen = set()
    rows = []

    for column in tree.find_all(exp.Column):
        table_alias = column.table
        table = alias_map.get(table_alias, table_alias or "<unqualified>")
        function, is_aggregate, _ = function_context_for_column(column)
        row = ColumnReference(table, column.name, clause_of(column), function, is_aggregate)
        if row not in seen:
            seen.add(row)
            rows.append(row)
    return rows


def outermost_select(node):
    if isinstance(node, exp.Union):
        return outermost_select(node.this)
    if isinstance(node, exp.Subquery):
        return outermost_select(node.this)
    if isinstance(node, exp.Select):
        return node
    inner = getattr(node, "this", None)
    return outermost_select(inner) if isinstance(inner, exp.Expression) else None


def extract_output_columns(sql: str, dialect: str = "tsql") -> list[OutputColumn]:
    tree = parse_sql(sql, dialect)
    select = outermost_select(tree)
    if not select:
        return []

    alias_map = build_alias_map(tree)
    output = []
    for projection in select.expressions:
        label = projection.alias_or_name
        expression_sql = projection.sql(dialect=dialect)
        sources = []
        seen = set()
        for column in projection.find_all(exp.Column):
            table_alias = column.table
            source = (alias_map.get(table_alias, table_alias or "<unqualified>"), column.name)
            if source not in seen:
                seen.add(source)
                sources.append(source)
        output.append(OutputColumn(label, expression_sql, tuple(sources)))
    return output
