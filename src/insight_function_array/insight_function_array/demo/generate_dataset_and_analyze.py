"""
Generate a synthetic business dataset, run it through the Insight Function Array,
render every compatible visualization, and save all artifacts.

Suggested location:
    insight_function_array/demo/generate_dataset_and_analyze.py

Run:
    python -m insight_function_array.demo.generate_dataset_and_analyze

Optional:
    python -m insight_function_array.demo.generate_dataset_and_analyze \
        --output .\\competitor_surprise_output \
        --seed 1807

Artifacts:
    generated_dataset.csv
    insights.csv
    insights.json
    run_manifest.json
    README.md
    visualizations/*.png
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import matplotlib

# A non-interactive backend is required for command-line and test execution.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from insight_function_array import detect_visualization_insights

try:
    # Present in the organized IFA package described by the project README.
    from insight_function_array.engine import render_visualization
except ImportError:
    # Some package versions expose it from the package root.
    from insight_function_array import render_visualization


DEFAULT_OUTPUT_DIR = Path("competitor_surprise_output")
DEFAULT_SEED = 1807


@dataclass(frozen=True)
class InsightRecord:
    dataset: str
    visualization: str
    visualization_file: str | None
    facet: str
    finding_key: str
    finding: str


def generate_dataset(seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """
    Create one denormalized BI-style dataset containing several overlapping
    business phenomena. The IFA is not told which phenomena were embedded.

    Embedded structure includes:
      * overall revenue growth followed by a late decline;
      * a competitor-driven loss concentrated in the Northwest;
      * stable revenue per retained customer;
      * increasing support volume;
      * increasing delivery delay;
      * falling gross margin;
      * product and channel mix differences;
      * ordinary noise and seasonality.

    The returned dataframe is intentionally row-level enough to support several
    useful grouped views.
    """
    rng = np.random.default_rng(seed)

    weeks = pd.date_range("2025-01-06", periods=78, freq="W-MON")
    regions = ["Northwest", "Southwest", "Midwest", "Northeast"]
    products = ["Core", "Professional", "Enterprise"]
    channels = ["Direct", "Partner", "Online"]

    rows: list[dict[str, Any]] = []

    for week_number, week in enumerate(weeks):
        seasonal = 1.0 + 0.08 * np.sin(2 * np.pi * week_number / 26)
        trend = 1.0 + 0.0045 * week_number

        # The external disruption begins late in the series.
        disruption_progress = max(0.0, (week_number - 53) / 18)
        disruption_progress = min(disruption_progress, 1.0)

        for region_number, region in enumerate(regions):
            region_factor = [1.12, 0.92, 1.00, 1.08][region_number]

            for product_number, product in enumerate(products):
                product_factor = [1.00, 0.72, 0.46][product_number]
                base_price = [110.0, 180.0, 330.0][product_number]
                base_margin_rate = [0.46, 0.52, 0.58][product_number]

                for channel_number, channel in enumerate(channels):
                    channel_factor = [1.00, 0.76, 0.88][channel_number]

                    competitor_pressure = 0.0
                    if region == "Northwest":
                        competitor_pressure = disruption_progress
                        if channel == "Online":
                            competitor_pressure *= 1.35
                        if product == "Core":
                            competitor_pressure *= 1.18

                    demand = (
                        1050
                        * region_factor
                        * product_factor
                        * channel_factor
                        * seasonal
                        * trend
                    )

                    # The lost customers are the main revenue effect.
                    customer_loss = 1.0 - 0.33 * competitor_pressure
                    active_customers = max(
                        20,
                        int(demand * customer_loss + rng.normal(0, 24)),
                    )

                    # Remaining-customer spend stays comparatively stable.
                    revenue_per_customer = base_price * (
                        1.0
                        + 0.012 * np.sin(week_number / 7)
                        + rng.normal(0, 0.012)
                    )
                    revenue = active_customers * revenue_per_customer

                    # Margin and operating measures develop related but distinct
                    # signals that may matter to analysts in other domains.
                    margin_pressure = 0.055 * competitor_pressure
                    gross_margin_rate = (
                        base_margin_rate
                        - margin_pressure
                        - 0.00045 * week_number
                        + rng.normal(0, 0.006)
                    )
                    gross_margin = revenue * gross_margin_rate

                    support_tickets = max(
                        0,
                        int(
                            active_customers * 0.055
                            + 35 * disruption_progress
                            + 18 * competitor_pressure
                            + rng.normal(0, 7)
                        ),
                    )

                    delivery_days = max(
                        0.5,
                        2.3
                        + 0.018 * week_number
                        + 1.4 * disruption_progress
                        + 0.45 * (channel == "Partner")
                        + rng.normal(0, 0.22),
                    )

                    satisfaction = np.clip(
                        4.55
                        - 0.09 * delivery_days
                        - 0.22 * competitor_pressure
                        + rng.normal(0, 0.08),
                        1.0,
                        5.0,
                    )

                    rows.append(
                        {
                            "Week": week,
                            "Region": region,
                            "Product": product,
                            "Channel": channel,
                            "ActiveCustomers": active_customers,
                            "Revenue": round(revenue, 2),
                            "RevenuePerCustomer": round(
                                revenue_per_customer, 2
                            ),
                            "GrossMargin": round(gross_margin, 2),
                            "GrossMarginRate": round(gross_margin_rate, 4),
                            "SupportTickets": support_tickets,
                            "AverageDeliveryDays": round(delivery_days, 2),
                            "CustomerSatisfaction": round(satisfaction, 3),
                        }
                    )

    return pd.DataFrame(rows)


def build_analytical_views(dataset: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Create representative dataframes similar to those produced through normal
    BI slicing and dicing.

    Each view is independently passed through the IFA. This matters because a
    single raw dataframe is not itself equivalent to the many grouped queries
    analysts produce.
    """
    views: dict[str, pd.DataFrame] = {}

    views["weekly_company"] = (
        dataset.groupby("Week", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            ActiveCustomers=("ActiveCustomers", "sum"),
            GrossMargin=("GrossMargin", "sum"),
            SupportTickets=("SupportTickets", "sum"),
            AverageDeliveryDays=("AverageDeliveryDays", "mean"),
            CustomerSatisfaction=("CustomerSatisfaction", "mean"),
        )
        .sort_values("Week")
    )
    views["weekly_company"]["RevenuePerCustomer"] = (
        views["weekly_company"]["Revenue"]
        / views["weekly_company"]["ActiveCustomers"]
    )
    views["weekly_company"]["GrossMarginRate"] = (
        views["weekly_company"]["GrossMargin"]
        / views["weekly_company"]["Revenue"]
    )

    views["weekly_by_region"] = (
        dataset.groupby(["Week", "Region"], as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            ActiveCustomers=("ActiveCustomers", "sum"),
            GrossMargin=("GrossMargin", "sum"),
            SupportTickets=("SupportTickets", "sum"),
            AverageDeliveryDays=("AverageDeliveryDays", "mean"),
        )
        .sort_values(["Week", "Region"])
    )

    views["revenue_by_region"] = (
        dataset.groupby("Region", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            GrossMargin=("GrossMargin", "sum"),
            ActiveCustomers=("ActiveCustomers", "sum"),
        )
        .sort_values("Revenue", ascending=False)
    )

    views["revenue_by_product"] = (
        dataset.groupby("Product", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            GrossMargin=("GrossMargin", "sum"),
            ActiveCustomers=("ActiveCustomers", "sum"),
        )
        .sort_values("Revenue", ascending=False)
    )

    views["revenue_by_channel"] = (
        dataset.groupby("Channel", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            GrossMargin=("GrossMargin", "sum"),
            ActiveCustomers=("ActiveCustomers", "sum"),
        )
        .sort_values("Revenue", ascending=False)
    )

    views["operations_scatter"] = (
        dataset.groupby(["Week", "Region"], as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            SupportTickets=("SupportTickets", "sum"),
            AverageDeliveryDays=("AverageDeliveryDays", "mean"),
            CustomerSatisfaction=("CustomerSatisfaction", "mean"),
            GrossMarginRate=("GrossMarginRate", "mean"),
        )
    )

    views["latest_region_snapshot"] = (
        dataset.loc[dataset["Week"] == dataset["Week"].max()]
        .groupby("Region", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            ActiveCustomers=("ActiveCustomers", "sum"),
            GrossMargin=("GrossMargin", "sum"),
            SupportTickets=("SupportTickets", "sum"),
            AverageDeliveryDays=("AverageDeliveryDays", "mean"),
            CustomerSatisfaction=("CustomerSatisfaction", "mean"),
        )
    )

    return views


def _slug(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return text.strip("_") or "artifact"


def _json_default(value: Any) -> Any:
    if isinstance(value, (pd.Timestamp, np.datetime64)):
        return pd.Timestamp(value).isoformat()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if pd.isna(value):
        return None
    return str(value)


def _write_csv_without_optional_dependencies(
    dataframe: pd.DataFrame, path: Path
) -> None:
    """
    Write CSV directly through pandas. Kept separate to emphasize that this
    runner does not require the optional `tabulate` package.
    """
    dataframe.to_csv(
        path,
        index=False,
        quoting=csv.QUOTE_NONNUMERIC,
        quotechar='"',
    )


def _normalize_findings(
    view_name: str,
    result: dict[str, Any],
    visualization_files: dict[str, str],
) -> list[InsightRecord]:
    records: list[InsightRecord] = []

    for key, finding in (result.get("findings") or {}).items():
        key_text = str(key)
        if " - " in key_text:
            visualization, facet = key_text.split(" - ", 1)
        else:
            visualization = "Unknown"
            facet = ""

        records.append(
            InsightRecord(
                dataset=view_name,
                visualization=visualization,
                visualization_file=visualization_files.get(visualization),
                facet=facet,
                finding_key=key_text,
                finding=str(finding),
            )
        )

    return records


def _save_figure(figure: plt.Figure, path: Path) -> None:
    figure.tight_layout()
    figure.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(figure)


def _render_one(
    dataframe: pd.DataFrame,
    visualization_name: str,
    output_path: Path,
) -> str | None:
    """
    Render through the package renderer while tolerating the renderer returning
    either an Axes or a Figure. Returns an error message rather than aborting the
    whole artifact run when one visualization cannot render.
    """
    plt.close("all")

    try:
        rendered = render_visualization(dataframe, visualization_name)

        if rendered is None:
            plt.close("all")
            return "Renderer returned no chart."

        if isinstance(rendered, plt.Figure):
            figure = rendered
        elif hasattr(rendered, "figure"):
            figure = rendered.figure
        else:
            figures = [plt.figure(number) for number in plt.get_fignums()]
            if not figures:
                return (
                    "Renderer returned an unsupported object and created no "
                    "matplotlib figure."
                )
            figure = figures[-1]

        _save_figure(figure, output_path)
        return None

    except Exception as exc:  # Continue so one chart does not lose all output.
        plt.close("all")
        return f"{type(exc).__name__}: {exc}"


def _markdown_table(dataframe: pd.DataFrame) -> str:
    """
    Minimal Markdown table writer. This deliberately avoids DataFrame.to_markdown
    so the demo does not depend on the optional `tabulate` package.
    """
    if dataframe.empty:
        return "_No rows._"

    display = dataframe.fillna("").astype(str)
    headers = [str(column).replace("|", r"\|") for column in display.columns]

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for row in display.itertuples(index=False, name=None):
        values = [
            str(value).replace("|", r"\|").replace("\n", " ")
            for value in row
        ]
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def run(
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    seed: int = DEFAULT_SEED,
) -> dict[str, Any]:
    output = Path(output_dir)
    visualizations_dir = output / "visualizations"
    views_dir = output / "analytical_views"

    output.mkdir(parents=True, exist_ok=True)
    visualizations_dir.mkdir(parents=True, exist_ok=True)
    views_dir.mkdir(parents=True, exist_ok=True)

    dataset = generate_dataset(seed)
    dataset_path = output / "generated_dataset.csv"
    _write_csv_without_optional_dependencies(dataset, dataset_path)

    views = build_analytical_views(dataset)

    all_records: list[InsightRecord] = []
    raw_results: dict[str, Any] = {}
    rendered_charts: list[dict[str, str]] = []
    render_errors: list[dict[str, str]] = []

    for view_name, dataframe in views.items():
        view_path = views_dir / f"{_slug(view_name)}.csv"
        _write_csv_without_optional_dependencies(dataframe, view_path)

        result = detect_visualization_insights(dataframe)
        raw_results[view_name] = result
        visualization_files: dict[str, str] = {}

        for visualization_name in result.get(
            "recommended_visualizations", []
        ):
            filename = (
                f"{_slug(view_name)}__"
                f"{_slug(str(visualization_name))}.png"
            )
            chart_path = visualizations_dir / filename

            error = _render_one(
                dataframe,
                str(visualization_name),
                chart_path,
            )

            if error:
                render_errors.append(
                    {
                        "dataset": view_name,
                        "visualization": str(visualization_name),
                        "error": error,
                    }
                )
            else:
                relative_chart_path = chart_path.relative_to(output).as_posix()
                visualization_files[str(visualization_name)] = (
                    relative_chart_path
                )
                rendered_charts.append(
                    {
                        "dataset": view_name,
                        "visualization": str(visualization_name),
                        "file": relative_chart_path,
                    }
                )

        all_records.extend(
            _normalize_findings(
                view_name,
                result,
                visualization_files,
            )
        )

    insights_df = pd.DataFrame(
        [asdict(record) for record in all_records],
        columns=[
            "dataset",
            "visualization",
            "visualization_file",
            "facet",
            "finding_key",
            "finding",
        ],
    )
    insights_path = output / "insights.csv"
    _write_csv_without_optional_dependencies(insights_df, insights_path)

    insights_json_path = output / "insights.json"
    insights_json_path.write_text(
        json.dumps(
            {
                "seed": seed,
                "insight_count": len(all_records),
                "insights": [asdict(record) for record in all_records],
                "raw_ifa_results": raw_results,
            },
            ensure_ascii=False,
            indent=2,
            default=_json_default,
        ),
        encoding="utf-8",
    )

    manifest = {
        "seed": seed,
        "output_directory": str(output.resolve()),
        "dataset_rows": int(len(dataset)),
        "analytical_view_count": len(views),
        "insight_count": len(all_records),
        "rendered_chart_count": len(rendered_charts),
        "render_error_count": len(render_errors),
        "files": {
            "dataset": str(dataset_path.relative_to(output)),
            "insights_csv": str(insights_path.relative_to(output)),
            "insights_json": str(insights_json_path.relative_to(output)),
            "analytical_views_directory": str(
                views_dir.relative_to(output)
            ),
            "visualizations_directory": str(
                visualizations_dir.relative_to(output)
            ),
        },
        "rendered_charts": rendered_charts,
        "render_errors": render_errors,
    }

    manifest_path = output / "run_manifest.json"
    manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
            default=_json_default,
        ),
        encoding="utf-8",
    )

    summary_rows = pd.DataFrame(
        [
            ["Generated dataset rows", len(dataset)],
            ["Analytical views", len(views)],
            ["Insights collected", len(all_records)],
            ["Charts rendered", len(rendered_charts)],
            ["Chart render errors", len(render_errors)],
        ],
        columns=["Artifact", "Count"],
    )

    chart_rows = pd.DataFrame(rendered_charts)
    error_rows = pd.DataFrame(render_errors)

    readme_sections = [
        "# Generated Dataset and IFA Analysis",
        "",
        (
            "This directory was produced by "
            "`generate_dataset_and_analyze.py`. The program generated one "
            "synthetic business dataset, created representative BI analytical "
            "views, passed every view through the Insight Function Array, "
            "rendered every recommended visualization, and collected all "
            "threshold-clearing findings."
        ),
        "",
        "## Run Summary",
        "",
        _markdown_table(summary_rows),
        "",
        "## Main Artifacts",
        "",
        "- `generated_dataset.csv` — complete generated source dataset",
        "- `analytical_views/` — grouped dataframes passed through the IFA",
        "- `visualizations/` — rendered recommended charts",
        "- `insights.csv` — normalized, one-finding-per-row output",
        "- `insights.json` — normalized findings plus raw IFA results",
        "- `run_manifest.json` — counts, paths, and rendering diagnostics",
        "",
        "## Rendered Visualizations",
        "",
        _markdown_table(chart_rows),
        "",
        "## Collected Insights",
        "",
        _markdown_table(insights_df),
    ]

    if not error_rows.empty:
        readme_sections.extend(
            [
                "",
                "## Visualization Render Errors",
                "",
                (
                    "These errors did not stop the remaining dataframes, "
                    "insight functions, or charts from being processed."
                ),
                "",
                _markdown_table(error_rows),
            ]
        )

    readme_path = output / "README.md"
    readme_path.write_text(
        "\n".join(readme_sections) + "\n",
        encoding="utf-8",
    )

    manifest["files"]["readme"] = str(readme_path.relative_to(output))
    manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
            default=_json_default,
        ),
        encoding="utf-8",
    )

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a synthetic dataset, create BI analytical views, run "
            "each through the Insight Function Array, render all recommended "
            "visualizations, and collect all findings."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=(
            "Artifact directory. Default: "
            f"{DEFAULT_OUTPUT_DIR}"
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help=f"Random seed. Default: {DEFAULT_SEED}",
    )
    args = parser.parse_args()

    report = run(args.output, args.seed)

    print("IFA artifact run complete.")
    print(f"Output: {report['output_directory']}")
    print(f"Dataset rows: {report['dataset_rows']}")
    print(f"Analytical views: {report['analytical_view_count']}")
    print(f"Insights: {report['insight_count']}")
    print(f"Charts: {report['rendered_chart_count']}")
    if report["render_error_count"]:
        print(
            "Chart render errors: "
            f"{report['render_error_count']} "
            "(see run_manifest.json)"
        )


if __name__ == "__main__":
    main()
