"""Run a small end-to-end demonstration."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from insight_function_array import (
    detect_visualization_insights,
    insights_to_markdown,
    render_recommended_visualizations,
)
from insight_function_array.demo.datasets import line_inflection, line_spikes, line_trend, scatter_corr_clusters

DATASETS = {
    "line_trend": line_trend,
    "line_spikes": line_spikes,
    "line_inflection": line_inflection,
    "scatter_corr_clusters": scatter_corr_clusters,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", choices=DATASETS, nargs="?", default="line_inflection")
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()

    dataframe = DATASETS[args.dataset]()
    insights = detect_visualization_insights(dataframe)
    print(insights_to_markdown(insights))

    if args.plot:
        render_recommended_visualizations(dataframe, max_charts=3)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
