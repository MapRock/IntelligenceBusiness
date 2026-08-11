# Insight Function Array — organized October 2025 code

This project organizes the code that accompanied the original Insight Function
Array work. It preserves the central design:

1. Infer the roles of columns in a BI-query dataframe.
2. Determine which common visualization types are compatible with it.
3. Run the simple insight functions associated with each compatible visualization.
4. Return recommended visualizations and threshold-clearing findings.
5. Normalize findings for later persistence in an ISG `QueryDef`.

## Structure

```text
src/insight_function_array/
├── engine.py             orchestration and optional rendering
├── columns.py            dataframe role inference
├── registry.py           dynamic analyzer discovery
├── settings.py           thresholds
├── statistics.py         robust z-score and clustering helpers
├── output.py             dataframe and Markdown output
├── catalog.py            discoverable @insight function metadata
├── analyzers/
│   ├── base.py           ChartAnalyzer and @insight metadata
│   ├── bar.py            dominance and dispersion
│   ├── histogram.py      skew and discreteness
│   ├── line.py           trend, spikes, inflection, intersections
│   ├── scatter.py        correlation and clustering
│   └── pie.py            applicability and rendering; no insight yet
├── sql/
│   ├── context.py        QueryDef-oriented SQL metadata extraction
│   └── lineage.py        stepwise outer-to-base column lineage
└── demo/
    ├── datasets.py       synthetic dataframes
    └── run_demo.py       command-line demonstration
```

All uploaded source files are preserved without modification under `legacy/`.

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[all]"
```

The SQL metadata modules require `sqlglot`; clustering requires
`scikit-learn`. Both are included by the `all` extra.

## Basic use

```python
from insight_function_array import detect_visualization_insights
from insight_function_array.demo.datasets import line_inflection

frame = line_inflection()
result = detect_visualization_insights(frame)
print(result)
```

The result retains the original shape:

```python
{
    "recommended_visualizations": ["Histogram", "Line Chart", ...],
    "findings": {
        "Line Chart - Sales": "Inflection around 2022-03-30 ...",
        ...
    },
}
```

## Demo

```bash
python -m insight_function_array.demo.run_demo line_inflection
python -m insight_function_array.demo.run_demo scatter_corr_clusters --plot
```

## Test

```bash
pytest
```

## Insight-function catalog

The October `@insight` annotations are now available programmatically:

```python
from insight_function_array import insight_function_catalog_dataframe

catalog = insight_function_catalog_dataframe()
print(catalog)
```

This table is a natural starting point for loading visualization types, insight
functions, purposes, and values into the knowledge graph.
