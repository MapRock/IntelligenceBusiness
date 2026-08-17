"""Bar-chart applicability, insight functions, and rendering."""

from __future__ import annotations

import numpy as np
import pandas as pd
import seaborn as sns

from ..settings import BAR_HIGH_CV, BAR_STD_REL_MAX, DOMINANCE_MIN_SHARE
from .base import ChartAnalyzer, insight


class BarChartAnalyzer(ChartAnalyzer):
    chart_name = "Bar Chart"

    def is_applicable(self, df, categorical_cols, numerical_cols, time_col):
        return len(categorical_cols) >= 1 and len(numerical_cols) >= 1

    @insight(
        what="A dominant category in the bar chart.",
        value="It is useful to know when there is an 800-pound gorilla.",
    )
    def _dominant_category(
        self,
        grouped: pd.Series,
        num_col: str,
        min_share: float | None = None,
    ) -> str | None:
        threshold = DOMINANCE_MIN_SHARE if min_share is None else min_share
        total = grouped.sum()
        if pd.isna(total) or total == 0:
            return None

        top_label = grouped.idxmax()
        share = float(grouped.loc[top_label]) / float(total)
        if share >= threshold:
            return f"{top_label} dominates the {num_col} metric ({share:.0%})."
        return None

    @insight(
        what="High dispersion among bars (large spread across categories).",
        value="Big differences between groups can indicate segmentation, outliers, or instability.",
    )
    def _high_dispersion(
        self,
        grouped: pd.Series,
        cat_col: str,
        num_col: str,
        min_cv: float | None = None,
        min_std_rel_max: float | None = None,
    ) -> str | None:
        mean_value = grouped.mean()
        std_value = grouped.std()
        max_value = grouped.max()

        threshold_cv = BAR_HIGH_CV if min_cv is None else min_cv
        threshold_relative = BAR_STD_REL_MAX if min_std_rel_max is None else min_std_rel_max

        if not np.isfinite(std_value):
            std_value = np.nan
        if not np.isfinite(mean_value):
            mean_value = np.nan
        if not np.isfinite(max_value):
            max_value = np.nan

        cv = (std_value / mean_value) if mean_value and np.isfinite(mean_value) else np.inf
        high_by_cv = np.isfinite(cv) and cv >= threshold_cv
        high_by_relative = (
            pd.notna(std_value)
            and pd.notna(max_value)
            and max_value != 0
            and std_value >= threshold_relative * max_value
        )

        if not (high_by_cv or high_by_relative):
            return None

        return (
            f"High dispersion in {num_col} across {cat_col} "
            f"(CV≈{cv:.0%}; std≈{std_value:.2f}, mean≈{mean_value:.2f})."
        )

    def analyze(self, df, categorical_cols, numerical_cols, time_col, add_finding):
        for cat_col in categorical_cols:
            for num_col in numerical_cols:
                grouped = df.groupby(cat_col, observed=True)[num_col].sum()
                if grouped.empty:
                    continue
                add_finding(self.chart_name, cat_col, self._dominant_category(grouped, num_col))
                add_finding(
                    self.chart_name,
                    cat_col,
                    self._high_dispersion(grouped, cat_col, num_col),
                )

    def plot(self, df, categorical_cols, numerical_cols, time_col, **kwargs):
        cat_col = kwargs.get("cat_col") or (categorical_cols[0] if categorical_cols else None)
        num_col = kwargs.get("num_col") or (numerical_cols[0] if numerical_cols else None)
        if not cat_col or not num_col:
            return None

        plot_df = (
            df.groupby(cat_col, observed=True)[num_col]
            .sum()
            .reset_index()
            .sort_values(num_col, ascending=False)
        )
        ax = sns.barplot(data=plot_df, x=cat_col, y=num_col)
        ax.set_title(f"{num_col} by {cat_col}")
        return ax
