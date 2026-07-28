# Insight Function Array — Tutorial

This tutorial shows how to set up and use the **Insight Function Array** package.  
It is the practical companion to the blog post on the Insight Space Graph and is intended to live alongside the code at:

```text
https://github.com/MapRock/IntelligenceBusiness/tree/main/src/insight_function_array
```

> **Note on layout**  
> The package follows the modern `src/` layout (`src/insight_function_array/`).  
> When this folder is placed inside the larger `IntelligenceBusiness` repository you will therefore see a second `src` directory. That is intentional and keeps the package installable in isolation while remaining easy to move or extract later.

---

## 1. Prerequisites

- Python 3.10 or newer
- `git` (optional, only if you clone the repository)
- A terminal (PowerShell, Command Prompt, macOS/Linux Terminal, or Windows Terminal)

---

## 2. Create and Activate a Virtual Environment

It is strongly recommended to work inside a virtual environment so the package and its dependencies stay isolated from your system Python.

### Windows (PowerShell or Command Prompt)

```powershell
# Navigate to the package root (the folder that contains pyproject.toml)
cd path\to\IntelligenceBusiness\src\insight_function_array

# Create the virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate
```

After activation your prompt should show `(.venv)`.

### macOS / Linux

```bash
cd path/to/IntelligenceBusiness/src/insight_function_array

python3 -m venv .venv
source .venv/bin/activate
```

### Deactivate later

```bash
deactivate
```

---

## 3. Install the Package

With the virtual environment activated, install the package in editable mode together with the optional extras you need:

```bash
# Core package only
pip install -e .

# Recommended: include clustering + SQL lineage support + test runner
pip install -e ".[all]"
```

The extras are:

| Extra        | What it adds                          |
|--------------|---------------------------------------|
| `clustering` | scikit-learn (KMeans + silhouette)    |
| `sql`        | sqlglot (QueryDef lineage helpers)    |
| `dev`        | pytest                                |
| `all`        | everything above                      |

---

## 4. Quick Smoke Test

```bash
python -c "from insight_function_array import detect_visualization_insights; print('OK')"
```

Or run the built-in tests:

```bash
pytest
```

---

## 5. Basic Usage

### 5.1 Detect insights from any DataFrame

```python
import pandas as pd
from insight_function_array import detect_visualization_insights, insights_to_markdown

# Load or create a DataFrame that looks like a typical BI query result
df = pd.read_csv("your_query_result.csv")   # or use one of the demo sets

result = detect_visualization_insights(df)

print(insights_to_markdown(result))
```

The returned dictionary always has the same shape:

```python
{
    "recommended_visualizations": ["Line Chart", "Histogram", ...],
    "findings": {
        "Line Chart - Sales": "Inflection around 2022-03-30 (sustained change).",
        "Bar Chart - Category": "D dominates the Sales metric (62%).",
        ...
    }
}
```

### 5.2 Turn findings into a tidy DataFrame (the “field notes ledger”)

```python
from insight_function_array import insights_to_dataframe

ledger = insights_to_dataframe(result)
print(ledger.head())
```

Useful columns include: `chart`, `facet`, `tags`, `score`, `date_hint`, `message`, etc.  
This ledger is the natural starting point for loading observations into an Insight Space Graph `QueryDef`.

### 5.3 Inspect the insight-function catalog

Every method decorated with `@insight` is discoverable:

```python
from insight_function_array import insight_function_catalog_dataframe

catalog = insight_function_catalog_dataframe()
print(catalog)
```

The catalog is ideal for seeding the knowledge graph with VisualizationType and InsightFunction nodes (`what` / `value` metadata).

---

## 6. Built-in Demo Datasets

A few synthetic data sets are included so you can exercise the detectors without real BI extracts:

```python
from insight_function_array.demo.datasets import (
    line_trend,
    line_spikes,
    line_inflection,
    scatter_corr_clusters,
)

df = line_inflection()
result = detect_visualization_insights(df)
print(insights_to_markdown(result))
```

You can also run them from the command line:

```bash
python -m insight_function_array.demo.run_demo line_inflection
python -m insight_function_array.demo.run_demo scatter_corr_clusters --plot
```

---

## 7. Rendering Charts (optional)

```python
from insight_function_array import render_recommended_visualizations
import matplotlib.pyplot as plt

axes = render_recommended_visualizations(df, max_charts=3)
plt.tight_layout()
plt.show()
```

Or render one chart by name:

```python
from insight_function_array import render_visualization

ax = render_visualization(df, "Line Chart", num_col="Sales")
```

---

## 8. SQL Lineage Helpers (optional extra)

When you have the original SQL that produced the dataframe, you can recover column lineage for the `QueryDef`:

```python
from insight_function_array.sql.lineage import analyze_sql_stepwise

sql = """
WITH Base AS (
    SELECT ProductKey, OrderDate, SalesAmount
    FROM dbo.FactInternetSales
)
SELECT ProductKey, SUM(SalesAmount) AS Sales
FROM Base
GROUP BY ProductKey
"""

rows = analyze_sql_stepwise(sql)
for role, name, chain in rows:
    print(f"{role:8} | {name:20} | {chain}")
```

This produces stepwise chains such as:

```text
Metric   | Sales               | Sales -> Base.SalesAmount -> dbo.FactInternetSales.SalesAmount
Dice     | ProductKey          | ProductKey -> Base.ProductKey -> dbo.FactInternetSales.ProductKey
```

These chains become the links from a `QueryDef` into the data catalog / semantic layer.

---

## 9. Typical Workflow Toward an Insight Space Graph

1. Capture (or reconstruct) the dataframe that an analyst’s BI tool returned.
2. Run `detect_visualization_insights(df)`.
3. Convert the findings with `insights_to_dataframe`.
4. Attach SQL lineage (if available) and column semantics from the governed catalog.
5. Persist the whole package as a `QueryDef` node in the Insight Space Graph, with relationships to:
   - the VisualizationType and InsightFunction nodes (from the catalog),
   - the business concepts that the columns resolve to,
   - time, analyst/service identity, and any later risk/opportunity assessments.

The observation layer is deliberately simple. Higher-order reasoning (induction, deduction, abduction, routing) can operate on the accumulated ledger without having to re-process the original data.

---


## 10. Next Steps

- Replace the synthetic data sets with real BI query extracts.
- Persist the tidy findings ledger + lineage into your graph store as `QueryDef` nodes.
- Load the insight-function catalog into the same knowledge graph so visualization types and detection functions become first-class concepts.
- Layer the LLM / symbolic reasoning (induction, deduction, abduction) on top of the accumulated observations.

That is the complete path from an ordinary BI dataframe to a shared, searchable observation fabric for the enterprise.

