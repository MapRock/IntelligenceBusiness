"""Pie-chart applicability and rendering.

The October 2025 implementation did not yet define pie-chart insight functions.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from .base import ChartAnalyzer


class PieChartAnalyzer(ChartAnalyzer):
    chart_name = "Pie Chart"

    def is_applicable(self, df, categorical_cols, numerical_cols, time_col):
        return len(categorical_cols) == 1 and len(numerical_cols) == 1

    def analyze(self, df, categorical_cols, numerical_cols, time_col, add_finding):
        return

    def plot(self, df, categorical_cols, numerical_cols, time_col, **kwargs):
        cat_col = kwargs.get("cat_col") or (categorical_cols[0] if categorical_cols else None)
        num_col = kwargs.get("num_col") or (numerical_cols[0] if numerical_cols else None)
        if not cat_col or not num_col:
            return None

        aggregate = df.groupby(cat_col, observed=True)[num_col].sum().reset_index()
        fig, ax = plt.subplots()
        ax.pie(
            aggregate[num_col].tolist(),
            labels=aggregate[cat_col].astype(str).tolist(),
            autopct="%1.1f%%",
            startangle=90,
        )
        ax.set_title(f"{num_col} share by {cat_col}")
        ax.axis("equal")
        return ax
