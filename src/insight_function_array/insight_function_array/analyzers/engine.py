"""Orchestrate compatible visualization selection and insight detection."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .columns import infer_columns
from .registry import get_analyzers


def _top_numeric_by_std(df: pd.DataFrame, columns: list[str], count: int) -> list[str]:
    candidates = [
        (column, pd.to_numeric(df[column], errors="coerce").std(skipna=True))
        for column in columns
    ]
    candidates = [
        (column, std)
        for column, std in candidates
        if pd.notna(std) and np.isfinite(std)
    ]
    candidates.sort(key=lambda item: item[1], reverse=True)
    return [column for column, _ in candidates[:count]]


def _best_corr_pair(df: pd.DataFrame, numerical_cols: list[str]):
    best_pair = None
    best_absolute_correlation = -1.0
    for index, first in enumerate(numerical_cols):
        for second in numerical_cols[index + 1 :]:
            correlation = pd.to_numeric(df[first], errors="coerce").corr(
                pd.to_numeric(df[second], errors="coerce")
            )
            if pd.notna(correlation) and abs(correlation) > best_absolute_correlation:
                best_absolute_correlation = abs(correlation)
                best_pair = (first, second)
    return best_pair


def detect_visualization_insights(df: pd.DataFrame) -> dict:
    """Recommend compatible visualizations and collect their simple findings."""
    categorical_cols, numerical_cols, time_col = infer_columns(df)
    if not numerical_cols:
        return {"error": "No numerical metrics available for visualization."}

    result = {"recommended_visualizations": [], "findings": {}}

    def add_finding(chart: str, facet: str, message: str | None) -> None:
        if not message:
            return
        key = f"{chart} - {facet}".strip()
        if key in result["findings"]:
            result["findings"][key] += " " + message
        else:
            result["findings"][key] = message

    analyzers = get_analyzers()
    recommendations = [
        analyzer.chart_name
        for analyzer in analyzers
        if analyzer.is_applicable(df, categorical_cols, numerical_cols, time_col)
    ]
    result["recommended_visualizations"] = list(dict.fromkeys(recommendations))

    for analyzer in analyzers:
        if analyzer.chart_name in result["recommended_visualizations"]:
            analyzer.analyze(
                df,
                categorical_cols,
                numerical_cols,
                time_col,
                add_finding,
            )

    return result


def render_visualization(df: pd.DataFrame, chart_name: str, **kwargs):
    """Render one visualization, choosing sensible columns when omitted."""
    categorical_cols, numerical_cols, time_col = infer_columns(df)
    auto_top_n = int(kwargs.pop("auto_top_n", 4))

    if chart_name == "Line Chart":
        wants_long = "hue" in kwargs and kwargs.get("num_col")
        has_wide = "num_cols" in kwargs or "num_col" in kwargs
        if not wants_long and not has_wide:
            picks = _top_numeric_by_std(df, numerical_cols, auto_top_n)
            if len(picks) >= 2:
                kwargs["num_cols"] = picks
            elif picks:
                kwargs["num_col"] = picks[0]

    elif chart_name == "Bar Chart":
        if "cat_col" not in kwargs and categorical_cols:
            def category_score(column):
                unique_count = df[column].nunique(dropna=True)
                return 3 <= unique_count <= 25, unique_count

            kwargs["cat_col"] = sorted(
                categorical_cols,
                key=category_score,
                reverse=True,
            )[0]
        if "num_col" not in kwargs and numerical_cols:
            picks = _top_numeric_by_std(df, numerical_cols, 1)
            if picks:
                kwargs["num_col"] = picks[0]

    elif chart_name == "Scatter Plot" and ("x" not in kwargs or "y" not in kwargs):
        if len(numerical_cols) >= 2:
            pair = _best_corr_pair(df, numerical_cols)
            kwargs["x"], kwargs["y"] = pair or (numerical_cols[0], numerical_cols[1])

    for analyzer in get_analyzers():
        if analyzer.chart_name == chart_name:
            plt.figure()
            return analyzer.plot(
                df,
                categorical_cols,
                numerical_cols,
                time_col,
                **kwargs,
            )

    raise ValueError(f"No analyzer registered for chart {chart_name!r}.")


def render_recommended_visualizations(
    df: pd.DataFrame,
    max_charts: int | None = None,
    **kwargs,
):
    """Render the visualizations recommended for a dataframe."""
    result = detect_visualization_insights(df)
    recommendations = result.get("recommended_visualizations", [])
    if max_charts is not None:
        recommendations = recommendations[:max_charts]

    axes = []
    for chart_name in recommendations:
        axis = render_visualization(df, chart_name, **kwargs)
        if axis is not None:
            axes.append(axis)
    return axes
