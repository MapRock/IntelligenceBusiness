"""Scatter-plot applicability, insight functions, and rendering."""

from __future__ import annotations

import pandas as pd
import seaborn as sns

from ..settings import CLUSTER_K_RANGE
from ..statistics import KMeans, SKLEARN_AVAILABLE, best_kmeans, standardize
from .base import ChartAnalyzer, insight


class ScatterPlotAnalyzer(ChartAnalyzer):
    chart_name = "Scatter Plot"

    def is_applicable(self, df, categorical_cols, numerical_cols, time_col):
        return len(numerical_cols) > 1

    @insight(
        what="A strong linear relationship between two numeric variables.",
        value="Correlation may reveal variables that move together, though it does not establish causation.",
    )
    def _correlation_finding(self, df, x: str, y: str) -> str | None:
        correlation = df[x].corr(df[y])
        if pd.notna(correlation) and abs(correlation) > 0.7:
            return f"Strong correlation detected ({correlation:.2f})."
        return None

    @insight(
        what="Distinct groups in a two-dimensional or high-dimensional numeric space.",
        value="Clusters may expose segments, operating modes, or populations that deserve separate interpretation.",
    )
    def _cluster_finding(self, values, dimensionality: int) -> str | None:
        labels, score, k = best_kmeans(values, CLUSTER_K_RANGE)
        if labels is None:
            return None
        if dimensionality == 2:
            return f"{k} clusters detected (silhouette {score:.2f})."
        return f"{k} clusters detected across {dimensionality}D (silhouette {score:.2f})."

    def analyze(self, df, categorical_cols, numerical_cols, time_col, add_finding):
        for index, x in enumerate(numerical_cols):
            for y in numerical_cols[index + 1 :]:
                add_finding(
                    self.chart_name,
                    f"{x} vs {y}",
                    self._correlation_finding(df, x, y),
                )

        if not SKLEARN_AVAILABLE:
            return

        for index, x in enumerate(numerical_cols):
            for y in numerical_cols[index + 1 :]:
                pair = df[[x, y]].dropna()
                if len(pair) < max(CLUSTER_K_RANGE) * 3:
                    continue
                values = standardize(pair[[x, y]].to_numpy(dtype=float))
                add_finding(
                    self.chart_name,
                    f"{x} vs {y}",
                    self._cluster_finding(values, 2),
                )

        if len(numerical_cols) >= 3:
            matrix = df[numerical_cols].dropna()
            if len(matrix) >= max(CLUSTER_K_RANGE) * 3:
                values = standardize(matrix.to_numpy(dtype=float))
                add_finding(
                    self.chart_name,
                    f"High-D ({len(numerical_cols)}D)",
                    self._cluster_finding(values, len(numerical_cols)),
                )

    def plot(self, df, categorical_cols, numerical_cols, time_col, **kwargs):
        x = kwargs.get("x")
        y = kwargs.get("y")
        dimensions = kwargs.get("dims")
        hue = kwargs.get("hue")
        cluster_k = kwargs.get("cluster_k")

        if dimensions and len(dimensions) >= 3:
            grid = sns.pairplot(df[dimensions].dropna())
            grid.fig.suptitle("Pairwise projections", y=1.02)
            return grid.axes[0][0]

        if not x or not y:
            if len(numerical_cols) < 2:
                return None
            x, y = numerical_cols[0], numerical_cols[1]

        plot_df = df[[x, y]].dropna().copy()
        if (
            hue == "cluster"
            and SKLEARN_AVAILABLE
            and cluster_k
            and cluster_k >= 2
            and len(plot_df) >= cluster_k * 3
        ):
            values = standardize(plot_df[[x, y]].to_numpy(dtype=float))
            model = KMeans(n_clusters=int(cluster_k), n_init=10, random_state=42).fit(values)
            plot_df["cluster"] = model.labels_.astype(str)
            ax = sns.scatterplot(data=plot_df, x=x, y=y, hue="cluster")
            ax.legend(title="cluster", bbox_to_anchor=(1.02, 1), loc="upper left")
        else:
            ax = sns.scatterplot(data=plot_df, x=x, y=y)

        if hue == "cluster" and cluster_k:
            ax.set_title(f"{int(cluster_k)} clusters: {x} vs {y}")
        else:
            ax.set_title(f"{x} vs {y}")

        ax.set_xlabel(x)
        ax.set_ylabel(y)
        return ax


