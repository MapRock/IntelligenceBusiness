
# Insight Function Array

The **Insight Function Array** is a component of the **Insight Space Graph (ISG)** architecture.

It applies a set of simple, explainable analytical functions to dataframes produced by ordinary BI queries. These dataframes resemble the tabular results generated when analysts use tools such as Tableau, Power BI, or similar analytics platforms to select dimensions and measures, apply filters, and choose levels of aggregation.

Each dataframe is evaluated against the visualization types for which it is suitable. The insight functions associated with those visualizations then look for the kinds of patterns a skilled analyst would normally notice.

Examples include:

- trends, spikes, inflection points, and intersections in line charts;
- dominant categories and high dispersion in bar charts;
- skewed or discrete distributions in histograms;
- correlations and clusters in scatter plots;
- composition and share in pie charts.

Insights that meet configured thresholds can be retained with query metadata in the Insight Space Graph.

## Why This Matters

Analysts across an enterprise work with many domains, systems, semantic models, and data sources. Each analyst usually has a local purpose.

An analyst may:

- overlook an insight in a complex visualization;
- see it but consider it irrelevant to the current task;
- recognize only one part of a wider pattern;
- work on a problem related to another analyst's work in a different domain.

The Insight Function Array captures qualifying insights whether or not the analyst notices or values them.

Stored centrally in the ISG, those insights can later be interpreted together across queries, domains, systems, and timespans. What appears insignificant in one analytical session may contribute to identifying a broader risk, opportunity, or emerging enterprise condition.

```text
BI query
    ↓
Dataframe
    ↓
Compatible visualization types
    ↓
Insight functions
    ↓
Detected insights
    ↓
QueryDef in the Insight Space Graph
    ↓
Cross-query interpretation
```

## Relationship to the Insight Space Graph

Each query is represented by a `QueryDef` node.

A `QueryDef` can retain or link to:

- selected dimensions and measures;
- filters and filter values;
- grouping and aggregation;
- time range;
- source tables and columns;
- semantic-layer and data-catalog objects;
- suitable visualization types;
- insight functions applied;
- detected insights and their scores or thresholds.

The Insight Function Array performs low-level detection. The ISG preserves context and relationships. Knowledge-graph and LLM-based reasoning can then interpret collections of insights as possible risks, opportunities, explanations, or recommended responses.

```text
BI system                  Calculates
Insight Function Array     Notices
Insight Space Graph        Remembers and connects
LLM or other reasoning     Interprets and advises
```

## Repository Location

The project is located at:

```text
C:\MapRock\IntelligenceBusiness\src\insight_function_array
```

The recommended virtual environment is located at the repository root:

```text
C:\MapRock\IntelligenceBusiness\.venv
```

## Project Structure

```text
insight_function_array\
├── pyproject.toml
├── README.md
├── tests\
└── src\
    └── insight_function_array\
        ├── __init__.py
        ├── catalog.py
        ├── columns.py
        ├── engine.py
        ├── output.py
        ├── registry.py
        ├── settings.py
        ├── statistics.py
        ├── analyzers\
        │   ├── base.py
        │   ├── bar.py
        │   ├── histogram.py
        │   ├── line.py
        │   ├── pie.py
        │   └── scatter.py
        ├── demo\
        │   ├── datasets.py
        │   └── run_demo.py
        └── sql\
            ├── context.py
            └── lineage.py
```

The outer `insight_function_array` directory is the installable project root. The inner `src\insight_function_array` directory is the Python import package.

## Environment Setup

Open PowerShell and move to the `IntelligenceBusiness` repository root:

```powershell
cd C:\MapRock\IntelligenceBusiness
```

Create and activate the virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Confirm the interpreter:

```powershell
python -c "import sys; print(sys.executable)"
```

The result should be:

```text
C:\MapRock\IntelligenceBusiness\.venv\Scripts\python.exe
```

Upgrade the packaging tools:

```powershell
python -m pip install --upgrade pip setuptools wheel
```

Move to the Insight Function Array project and install it in editable mode:

```powershell
cd C:\MapRock\IntelligenceBusiness\src\insight_function_array
python -m pip install -e ".[all]"
```

Editable mode allows source-code changes to take effect without reinstalling the package.

## Run the Demonstration

```powershell
python -m insight_function_array.demo.run_demo line_inflection
```

Other generated demonstration datasets may include:

```text
baseline
line_trend
line_spikes
line_inflection
line_intersections_wide
scatter_corr_clusters
line_long_by_region
```

For example:

```powershell
python -m insight_function_array.demo.run_demo scatter_corr_clusters
```

## Run the Tests

```powershell
python -m pytest
```

## Basic Python Usage

```python
import pandas as pd

from insight_function_array import detect_visualization_insights

df = pd.read_csv("my_query_result.csv")
insights = detect_visualization_insights(df)

print(insights["recommended_visualizations"])

for key, message in insights["findings"].items():
    print(f"{key}: {message}")
```

The current result structure is:

```python
{
    "recommended_visualizations": [
        "Line Chart",
        "Scatter Plot"
    ],
    "findings": {
        "Line Chart - Sales": "Strong trend detected in Sales over Date.",
        "Scatter Plot - Sales vs Profit": "Strong correlation detected (0.92)."
    }
}
```

## Producing a Dataframe of Insights

```python
from insight_function_array import (
    detect_visualization_insights,
    insights_to_dataframe,
)

insights = detect_visualization_insights(df)
insights_df = insights_to_dataframe(insights)

print(insights_df)
```

The normalized dataframe can contain fields such as:

- chart;
- facet;
- metric;
- metric pairs;
- intersecting series;
- human-readable message;
- tags;
- score;
- date hint;
- recommendation status.

## Rendering Recommended Visualizations

```python
import matplotlib.pyplot as plt

from insight_function_array import render_recommended_visualizations

render_recommended_visualizations(df, max_charts=3)
plt.show()
```

The visualization engine chooses sensible default columns when explicit parameters are not supplied.

## Current Analyzer Modules

### Line Chart

The line-chart analyzer currently looks for:

- strong trends;
- spikes;
- inflection points;
- intersections among multiple numeric series.

A line chart is applicable when the dataframe contains a detectable time-like column.

### Bar Chart

The bar-chart analyzer currently looks for:

- a dominant category;
- high dispersion across categories.

A bar chart is applicable when the dataframe contains at least one categorical column and one numeric column.

### Histogram

The histogram analyzer currently looks for:

- highly skewed distributions;
- discrete or low-cardinality numeric distributions.

A histogram is applicable when the dataframe contains at least one numeric column.

### Scatter Plot

The scatter-plot analyzer currently looks for:

- strong pairwise correlations;
- two-dimensional clusters;
- higher-dimensional clusters across several numeric columns.

Clustering is available when `scikit-learn` is installed.

### Pie Chart

The pie-chart analyzer currently supports applicability and rendering for a dataframe with one categorical and one numeric column.

Its insight-detection functions are not yet implemented.

## Insight Metadata Catalog

Insight functions can be annotated with metadata describing:

- what the function detects;
- why the finding may matter.

For example:

```python
@insight(
    what="A dominant category in the bar chart.",
    value="It is useful to know when one category behaves as an 800-pound gorilla.",
)
def detect_dominant_category(...):
    ...
```

The catalog module can expose those annotations as structured metadata suitable for documentation or knowledge-graph loading.

```text
VisualizationType
    supportsInsightFunction
        InsightFunction

InsightFunction
    detects
        InsightType
```

This allows visualization types and their insight functions to become part of the knowledge graph rather than remaining only implicit in Python code.

## SQL and QueryDef Metadata

The `sql` package supports analysis of SQL text used to produce a dataframe.

Current capabilities include:

- identifying columns referenced in `SELECT`, `WHERE`, `HAVING`, `GROUP BY`, `ORDER BY`, joins, and window expressions;
- identifying aggregate-function context;
- mapping aliases to source tables;
- mapping outer selected columns to source columns;
- tracing stepwise column lineage through CTEs and subqueries;
- classifying selected items as metrics, dice dimensions, filters, or other selected values.

These functions are intended to help construct the metadata attached to a `QueryDef`.

Example conceptual output:

```text
Metric :: SalesAmount ::
    SalesAmount
    -> Base.SalesAmount
    -> dbo.FactInternetSales.SalesAmount
```

The SQL functions use `sqlglot`.

## Column Inference

The engine infers three broad dataframe roles:

- categorical columns;
- numerical columns;
- a time-like column.

Object and category columns are treated as categorical. Low-cardinality numeric columns may also be treated as possible categories while remaining available as numeric metrics.

Time-like columns are inferred primarily from names containing terms such as `date`, `time`, `timestamp`, or `dt`. When possible, those columns are converted to Pandas datetime values.

This is currently heuristic and can be replaced or supplemented by explicit `QueryDef` or semantic-layer metadata.

## Thresholds and Settings

Detection thresholds are centralized in the project settings and statistical utilities.

Examples include:

- robust z-score threshold for spikes;
- inflection-point window;
- inflection magnitude;
- sustained-run length;
- minimum dominant-category share;
- cluster range;
- minimum silhouette score.

Thresholds should eventually be configurable by visualization type, insight function, domain, measure, user or organizational policy, and sensitivity profile.

## Adding a New Analyzer

Create a new analyzer in:

```text
src\insight_function_array\analyzers
```

Subclass `ChartAnalyzer`:

```python
from insight_function_array.analyzers.base import ChartAnalyzer


class ExampleAnalyzer(ChartAnalyzer):
    chart_name = "Example Chart"

    def is_applicable(
        self,
        df,
        categorical_cols,
        numerical_cols,
        time_col,
    ):
        return True

    def analyze(
        self,
        df,
        categorical_cols,
        numerical_cols,
        time_col,
        add_finding,
    ):
        add_finding(
            self.chart_name,
            "Example",
            "Example insight detected.",
        )

    def plot(
        self,
        df,
        categorical_cols,
        numerical_cols,
        time_col,
        **kwargs,
    ):
        raise NotImplementedError
```

The registry discovers analyzer classes from the analyzer package.

## Adding a New Insight Function

An insight function should ideally:

1. represent one understandable analytical observation;
2. be associated with a visualization type;
3. state its applicability conditions;
4. use an explicit and configurable threshold;
5. return structured evidence in addition to a human-readable message;
6. preserve the columns and values involved;
7. expose metadata describing what it detects and why it matters.

The current implementation still returns mostly human-readable findings. A future refinement is to make each finding a structured object before rendering it as text.

Possible fields include:

```text
insight_type
visualization_type
function_name
columns
values
magnitude
score
threshold
start_time
end_time
detected_at
explanation
```

## Current Limitations

This project is an experimental implementation of the Insight Function Array concept.

Current limitations include:

- visualization applicability is heuristic;
- many findings are represented as text rather than typed objects;
- thresholds are general rather than domain-specific;
- the pie-chart analyzer has no implemented insight functions;
- the line-chart analyzer currently emphasizes time-series structure but not seasonality or spectral decomposition;
- strong correlation does not establish causation;
- clustering results require interpretation;
- SQL lineage is best-effort and may not resolve every complex query;
- the package does not yet write `QueryDef` nodes directly to a graph database;
- LLM interpretation and risk/opportunity reasoning are outside the current package.

## Near-Term Development Directions

Potential next steps include:

- structured `Insight` and `QueryDef` data classes;
- direct export to RDF or another graph representation;
- an ontology for visualization types, insight functions, and insight types;
- additional line-chart functions for seasonality, Fourier components, volatility, and change points;
- additional scatter-plot functions for nonlinear relationships and outliers;
- composition insights for pie and stacked charts;
- heat-map and box-plot analyzers;
- semantic-layer and data-catalog mappings;
- threshold profiles by domain and measure;
- graph retrieval of related insights across domains and timespans;
- LLM interpretation of selected ISG neighborhoods;
- conversion of repeated recommendations into decision rules or process guidance.

## Development Workflow

At the start of a new PowerShell session:

```powershell
cd C:\MapRock\IntelligenceBusiness
.\.venv\Scripts\Activate.ps1
cd .\src\insight_function_array
```

Run tests during development:

```powershell
python -m pytest
```

Confirm the installed package location:

```powershell
python -c "import insight_function_array; print(insight_function_array.__file__)"
```

The path should resolve beneath:

```text
C:\MapRock\IntelligenceBusiness\src\insight_function_array\src\insight_function_array
```

## Git Ignore

The repository-level `.gitignore` should include:

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
*.egg-info/
dist/
build/
```

## Background

The Insight Function Array is part of the broader Enterprise Intelligence and Insight Space Graph work.

Background reading:

```text
https://eugeneasahara.com/2022/03/21/insight-space-graph/
```
