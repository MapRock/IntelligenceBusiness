"""Insight Function Array.

The package keeps the original public result shape:

    {
        "recommended_visualizations": [...],
        "findings": {"Chart - Facet": "message", ...},
    }
"""

from .engine import (
    detect_visualization_insights,
    infer_columns,
    render_recommended_visualizations,
    render_visualization,
)
from .catalog import get_insight_function_catalog, insight_function_catalog_dataframe
from .output import insights_to_dataframe, insights_to_markdown, recommendations_to_dataframe

__all__ = [
    "detect_visualization_insights",
    "infer_columns",
    "render_visualization",
    "render_recommended_visualizations",
    "insights_to_dataframe",
    "insights_to_markdown",
    "recommendations_to_dataframe",
    "get_insight_function_catalog",
    "insight_function_catalog_dataframe",
]
