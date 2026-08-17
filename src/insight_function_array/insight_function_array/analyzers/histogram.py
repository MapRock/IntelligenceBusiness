"""Histogram applicability, insight functions, and rendering."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .base import ChartAnalyzer, insight


class HistogramAnalyzer(ChartAnalyzer):
    chart_name = "Histogram"

    def is_applicable(self, df, categorical_cols, numerical_cols, time_col):
        return len(numerical_cols) >= 1

    @insight(
        what="A substantially skewed numeric distribution.",
        value="Skew may expose concentration, a long tail, or unusual extremes.",
    )
    def _skew_finding(self, series: pd.Series, num_col: str) -> str | None:
        skewness = series.skew()
        if pd.notna(skewness) and abs(skewness) > 1:
            return f"Skewed distribution detected in {num_col}."
        return None

    @insight(
        what="A numeric column with relatively few distinct values.",
        value="A discrete distribution may represent counts, ratings, or encoded categories.",
    )
    def _discrete_finding(self, series: pd.Series, num_col: str) -> str | None:
        if series.nunique(dropna=True) < 10:
            return f"Discrete distribution detected in {num_col}."
        return None

    def analyze(self, df, categorical_cols, numerical_cols, time_col, add_finding):
        for num_col in numerical_cols:
            messages = [
                self._skew_finding(df[num_col], num_col),
                self._discrete_finding(df[num_col], num_col),
            ]
            message = " ".join(item for item in messages if item)
            add_finding(self.chart_name, num_col, message or None)

    def plot(self, df, categorical_cols, numerical_cols, time_col, **kwargs):
        num_col = kwargs.get("num_col") or (numerical_cols[0] if numerical_cols else None)
        if not num_col:
            return None

        series = (
            pd.to_numeric(df[num_col], errors="coerce")
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
        )
        ax = plt.gca()
        ax.hist(series, bins="auto")
        ax.set_title(f"Distribution of {num_col}")
        ax.set_xlabel(num_col)
        ax.set_ylabel("Count")
        return ax
