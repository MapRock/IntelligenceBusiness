"""A cross-domain Insight Space Graph demonstration.

This fictional scenario shows how locally useful BI investigations can produce
small, explainable insights that become more valuable when retained together.
The final competitor explanation is not present in any one query.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..engine import detect_visualization_insights
from ..output import insights_to_dataframe


LAUNCH_DATE = pd.Timestamp("2026-03-16")
COMPETITOR_NAME = "ApexOne"


@dataclass
class ScenarioQuery:
    query_id: str
    domain: str
    analyst_question: str
    data_source: str
    selected_visualization: str
    analyst_cares_about: str
    locally_ignored_or_missed: str
    dataframe: pd.DataFrame
    selected_finding_prefixes: tuple[str, ...]

    def metadata(self) -> dict:
        return {
            "query_id": self.query_id,
            "domain": self.domain,
            "analyst_question": self.analyst_question,
            "data_source": self.data_source,
            "selected_visualization": self.selected_visualization,
            "columns": list(self.dataframe.columns),
            "analyst_cares_about": self.analyst_cares_about,
            "locally_ignored_or_missed": self.locally_ignored_or_missed,
        }


def _weekly_dates() -> pd.DatetimeIndex:
    return pd.date_range("2026-01-05", periods=20, freq="W-MON")


def build_sales_query(rng: np.random.Generator) -> ScenarioQuery:
    dates = _weekly_dates()
    pre_count = 10
    active_customers = np.array(
        [1000 + rng.normal(0, 8) for _ in range(pre_count)]
        + [930 - 35 * i + rng.normal(0, 6) for i in range(10)]
    )
    average_revenue = np.array([250 + rng.normal(0, 2) for _ in dates])
    revenue = active_customers * average_revenue
    new_customers = np.array(
        [90 + rng.normal(0, 4) for _ in range(pre_count)]
        + [55 - 2 * i + rng.normal(0, 3) for i in range(10)]
    )

    dataframe = pd.DataFrame(
        {
            "WeekStartDate": dates,
            "Revenue": revenue.round(0).astype(int),
            "ActiveCustomers": active_customers.round(0).astype(int),
            "AvgRevenuePerCustomer": average_revenue.round(2),
            "NewCustomers": new_customers.round(0).astype(int),
        }
    )
    return ScenarioQuery(
        query_id="QD-SALES-001",
        domain="Sales",
        analyst_question="Why did weekly revenue suddenly fall?",
        data_source="Sales semantic model",
        selected_visualization="Indexed line chart",
        analyst_cares_about=(
            "Revenue and active-customer decline, plus whether the decline is "
            "concentrated in new or existing customers."
        ),
        locally_ignored_or_missed=(
            "Average revenue per remaining customer is stable. By itself that is "
            "not the sales analyst's main problem, but it argues against lower "
            "spending by retained customers."
        ),
        dataframe=dataframe,
        selected_finding_prefixes=(
            "Line Chart - Revenue",
            "Line Chart - ActiveCustomers",
            "Line Chart - AvgRevenuePerCustomer",
            "Line Chart - NewCustomers",
            "Scatter Plot - Revenue vs ActiveCustomers",
        ),
    )


def build_marketing_query(rng: np.random.Generator) -> ScenarioQuery:
    dates = _weekly_dates()
    pre_count = 10
    paid_search_cpc = np.array(
        [2.8 + rng.normal(0, 0.05) for _ in range(pre_count)]
        + [3.6 + 0.2 * i + rng.normal(0, 0.05) for i in range(10)]
    )
    lost_impression_share = np.array(
        [0.18 + rng.normal(0, 0.01) for _ in range(pre_count)]
        + [0.35 + 0.025 * i + rng.normal(0, 0.01) for i in range(10)]
    )
    landing_page_conversion = np.array(
        [0.118 + rng.normal(0, 0.003) for _ in dates]
    )
    apex_searches = np.array(
        [3 + rng.integers(-1, 2) for _ in range(pre_count)]
        + [80 + 10 * i + rng.integers(-2, 3) for i in range(10)]
    )

    dataframe = pd.DataFrame(
        {
            "WeekStartDate": dates,
            "PaidSearchCPC": paid_search_cpc.round(2),
            "LostImpressionShare": lost_impression_share.round(3),
            "LandingPageConversionRate": landing_page_conversion.round(3),
            "ApexOneSearches": apex_searches.astype(int),
        }
    )
    return ScenarioQuery(
        query_id="QD-MKT-001",
        domain="Marketing",
        analyst_question="Why has paid acquisition become less efficient?",
        data_source="Digital marketing semantic model",
        selected_visualization="Line charts",
        analyst_cares_about=(
            "The abrupt increase in cost per click and lost impression share, "
            "and whether the landing page stopped converting."
        ),
        locally_ignored_or_missed=(
            "Searches for the unfamiliar name ApexOne are still small compared "
            "with total category traffic, but their relative increase is enormous."
        ),
        dataframe=dataframe,
        selected_finding_prefixes=(
            "Line Chart - PaidSearchCPC",
            "Line Chart - LostImpressionShare",
            "Line Chart - LandingPageConversionRate",
            "Line Chart - ApexOneSearches",
            "Scatter Plot - PaidSearchCPC vs ApexOneSearches",
            "Scatter Plot - LostImpressionShare vs ApexOneSearches",
        ),
    )


def build_customer_success_query() -> ScenarioQuery:
    dataframe = pd.DataFrame(
        {
            "CancellationReason": [
                "Switched to another provider",
                "Budget reduction",
                "Missing feature",
                "Service issue",
                "Business closed",
                "Other",
            ],
            "Cancellations": [182, 38, 27, 18, 14, 21],
        }
    )
    return ScenarioQuery(
        query_id="QD-CS-001",
        domain="Customer Success",
        analyst_question="Are service or support problems driving cancellations?",
        data_source="Customer-success semantic model",
        selected_visualization="Bar chart",
        analyst_cares_about=(
            "The cancellation reasons that customer-success and support teams can "
            "directly address."
        ),
        locally_ignored_or_missed=(
            "'Switched to another provider' is often treated as a vague, externally "
            "caused bucket rather than an operational finding owned by the team."
        ),
        dataframe=dataframe,
        selected_finding_prefixes=("Bar Chart - CancellationReason",),
    )


def build_operations_query(rng: np.random.Generator) -> ScenarioQuery:
    dates = _weekly_dates()
    dataframe = pd.DataFrame(
        {
            "WeekStartDate": dates,
            "UptimePct": np.array(
                [99.95 + rng.normal(0, 0.015) for _ in dates]
            ).round(3),
            "MedianResponseMs": np.array(
                [220 + rng.normal(0, 4) for _ in dates]
            ).round(1),
            "FulfillmentDays": np.array(
                [2.10 + rng.normal(0, 0.04) for _ in dates]
            ).round(2),
            "PriceIndex": np.array(
                [100 + rng.normal(0, 0.15) for _ in dates]
            ).round(2),
            "SupportResolutionHours": np.array(
                [10 + rng.normal(0, 0.25) for _ in dates]
            ).round(2),
        }
    )
    return ScenarioQuery(
        query_id="QD-OPS-001",
        domain="Operations and Product",
        analyst_question="Did price, reliability, service, or fulfillment deteriorate?",
        data_source="Operations and product semantic models",
        selected_visualization="Indexed line chart",
        analyst_cares_about=(
            "Whether an internal operating or product change coincided with the "
            "customer loss."
        ),
        locally_ignored_or_missed=(
            "The analyst finds no operational problem and closes the investigation. "
            "In the wider ISG, that stability is valuable negative evidence."
        ),
        dataframe=dataframe,
        selected_finding_prefixes=(
            "Line Chart - UptimePct",
            "Line Chart - MedianResponseMs",
            "Line Chart - FulfillmentDays",
            "Line Chart - PriceIndex",
            "Line Chart - SupportResolutionHours",
        ),
    )


def build_scenario(seed: int = 42) -> list[ScenarioQuery]:
    rng = np.random.default_rng(seed)
    return [
        build_sales_query(rng),
        build_marketing_query(rng),
        build_customer_success_query(),
        build_operations_query(rng),
    ]


def _selected_insights(query: ScenarioQuery, insights: dict) -> pd.DataFrame:
    dataframe = insights_to_dataframe(insights)
    if dataframe.empty:
        return dataframe
    mask = pd.Series(False, index=dataframe.index)
    for prefix in query.selected_finding_prefixes:
        mask |= dataframe["key"].str.startswith(prefix, na=False)
    selected = dataframe.loc[mask].copy()
    selected.insert(0, "query_id", query.query_id)
    selected.insert(1, "domain", query.domain)
    return selected


def _baseline_index(dataframe: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    result = dataframe[["WeekStartDate"] + columns].copy()
    pre_launch = result[result["WeekStartDate"] < LAUNCH_DATE]
    for column in columns:
        baseline = pd.to_numeric(pre_launch[column], errors="coerce").mean()
        result[column] = pd.to_numeric(result[column], errors="coerce") / baseline * 100
    return result


def _save_indexed_line_chart(
    dataframe: pd.DataFrame,
    columns: list[str],
    title: str,
    path: Path,
) -> None:
    indexed = _baseline_index(dataframe, columns)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for column in columns:
        ax.plot(indexed["WeekStartDate"], indexed[column], marker="o", label=column)
    ax.axvline(LAUNCH_DATE, linestyle="--", linewidth=1)
    ax.text(LAUNCH_DATE, ax.get_ylim()[1], " Competitor launch", va="top")
    ax.set_title(title)
    ax.set_ylabel("Index: pre-launch average = 100")
    ax.set_xlabel("Week")
    ax.legend(loc="best")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _save_single_line_chart(
    dataframe: pd.DataFrame,
    column: str,
    title: str,
    path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(dataframe["WeekStartDate"], dataframe[column], marker="o")
    ax.axvline(LAUNCH_DATE, linestyle="--", linewidth=1)
    ax.text(LAUNCH_DATE, ax.get_ylim()[1], " Competitor launch", va="top")
    ax.set_title(title)
    ax.set_ylabel(column)
    ax.set_xlabel("Week")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _save_bar_chart(dataframe: pd.DataFrame, path: Path) -> None:
    plot_df = dataframe.sort_values("Cancellations", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(plot_df["CancellationReason"], plot_df["Cancellations"])
    ax.set_title("Cancellations by reported reason")
    ax.set_xlabel("Cancellations")
    ax.set_ylabel("Cancellation reason")
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _write_charts(queries: list[ScenarioQuery], output_dir: Path) -> dict[str, list[str]]:
    chart_files: dict[str, list[str]] = {}
    for query in queries:
        if query.query_id == "QD-SALES-001":
            path = output_dir / "qd_sales_001.png"
            _save_indexed_line_chart(
                query.dataframe,
                ["Revenue", "ActiveCustomers", "AvgRevenuePerCustomer", "NewCustomers"],
                "Sales investigation: customers disappear while spend per customer holds",
                path,
            )
            chart_files[query.query_id] = [path.name]
        elif query.query_id == "QD-MKT-001":
            path1 = output_dir / "qd_mkt_001_acquisition.png"
            _save_indexed_line_chart(
                query.dataframe,
                ["PaidSearchCPC", "LostImpressionShare", "LandingPageConversionRate"],
                "Marketing investigation: auction pressure rises while conversion holds",
                path1,
            )
            path2 = output_dir / "qd_mkt_001_apexone_searches.png"
            _save_single_line_chart(
                query.dataframe,
                "ApexOneSearches",
                "A small search term that suddenly becomes significant",
                path2,
            )
            chart_files[query.query_id] = [path1.name, path2.name]
        elif query.query_id == "QD-CS-001":
            path = output_dir / "qd_cs_001.png"
            _save_bar_chart(query.dataframe, path)
            chart_files[query.query_id] = [path.name]
        elif query.query_id == "QD-OPS-001":
            path = output_dir / "qd_ops_001.png"
            _save_indexed_line_chart(
                query.dataframe,
                [
                    "UptimePct",
                    "MedianResponseMs",
                    "FulfillmentDays",
                    "PriceIndex",
                    "SupportResolutionHours",
                ],
                "Operations investigation: internal conditions remain stable",
                path,
            )
            chart_files[query.query_id] = [path.name]
    return chart_files


def build_isg_evidence_table(selected_insights: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Evidence": "Revenue and active customers change together",
                "SourceQueryDef": "QD-SALES-001",
                "LocalMeaning": "Sales has a serious decline.",
                "WiderMeaning": "The loss is primarily customer disappearance rather than smaller purchases.",
            },
            {
                "Evidence": "Average revenue per remaining customer is stable",
                "SourceQueryDef": "QD-SALES-001",
                "LocalMeaning": "Not the primary sales concern.",
                "WiderMeaning": "Argues against a broad reduction in customer spending or an internal price change.",
            },
            {
                "Evidence": "Paid-search cost and lost impression share jump",
                "SourceQueryDef": "QD-MKT-001",
                "LocalMeaning": "Paid acquisition has become more expensive.",
                "WiderMeaning": "Suggests sudden external bidding or market pressure.",
            },
            {
                "Evidence": "Landing-page conversion remains stable",
                "SourceQueryDef": "QD-MKT-001",
                "LocalMeaning": "The campaign page is probably not broken.",
                "WiderMeaning": "Argues against an internal funnel failure as the main cause.",
            },
            {
                "Evidence": "Searches for ApexOne rise abruptly",
                "SourceQueryDef": "QD-MKT-001",
                "LocalMeaning": "A small unfamiliar term within a much larger search dataset.",
                "WiderMeaning": "Provides a candidate external entity connected to the same change window.",
            },
            {
                "Evidence": "Switched to another provider dominates cancellations",
                "SourceQueryDef": "QD-CS-001",
                "LocalMeaning": "Most cancellations are outside support's direct control.",
                "WiderMeaning": "Strong evidence of competitive displacement rather than service failure.",
            },
            {
                "Evidence": "Price, reliability, fulfillment, and support remain stable",
                "SourceQueryDef": "QD-OPS-001",
                "LocalMeaning": "Operations finds no incident to correct.",
                "WiderMeaning": "Negative evidence that removes several internal explanations.",
            },
        ]
    )


def build_kg_context_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"Subject": COMPETITOR_NAME, "Relationship": "rdf:type", "Object": "Competitor"},
            {"Subject": COMPETITOR_NAME, "Relationship": "targetsSegment", "Object": "Mid-market customers"},
            {"Subject": COMPETITOR_NAME, "Relationship": "fundingAmount", "Object": "$180 million"},
            {"Subject": COMPETITOR_NAME, "Relationship": "launchDate", "Object": LAUNCH_DATE.date().isoformat()},
            {"Subject": COMPETITOR_NAME, "Relationship": "offers", "Object": "Subsidized pricing and rapid onboarding"},
        ]
    )


def _markdown_table(dataframe: pd.DataFrame) -> str:
    if dataframe.empty:
        return "_No rows._"
    return dataframe.to_markdown(index=False)


def _write_blog_assets_markdown(
    queries: list[ScenarioQuery],
    selected_by_query: dict[str, pd.DataFrame],
    chart_files: dict[str, list[str]],
    evidence: pd.DataFrame,
    kg_context: pd.DataFrame,
    output_dir: Path,
) -> Path:
    lines = [
        "# The Competitor We Did Not See",
        "",
        "> Fictional demonstration data for the Insight Function Array.",
        "",
        "Weekly sales suddenly fall. Nothing obvious inside the company changed. "
        "Sales, marketing, customer success, and operations investigate independently, "
        "each using the data and visualizations natural to that domain. No analyst begins "
        "with the hypothesis that a heavily funded competitor launched at national scale.",
        "",
        "The point of the example is not that any one simple function discovers the cause. "
        "The functions capture small insights. The Insight Space Graph retains their query "
        "context, links the data components to enterprise meaning, and makes the collection "
        "available for wider interpretation.",
        "",
    ]

    for query in queries:
        lines.extend(
            [
                f"## {query.query_id}: {query.domain}",
                "",
                f"**Analyst question:** {query.analyst_question}",
                "",
                f"**What the analyst cares about:** {query.analyst_cares_about}",
                "",
                f"**What may be ignored or missed locally:** {query.locally_ignored_or_missed}",
                "",
            ]
        )
        for filename in chart_files.get(query.query_id, []):
            lines.extend([f"![{query.domain} visualization]({filename})", ""])

        display_data = query.dataframe.copy()
        for col in display_data.columns:
            if pd.api.types.is_datetime64_any_dtype(display_data[col]):
                display_data[col] = display_data[col].dt.date.astype(str)
        lines.extend(
            [
                "### Data returned by the query",
                "",
                _markdown_table(display_data),
                "",
                "### Insights retained for this example",
                "",
                _markdown_table(
                    selected_by_query[query.query_id][
                        ["chart", "facet", "message", "tags", "score", "date_hint"]
                    ]
                    if not selected_by_query[query.query_id].empty
                    else selected_by_query[query.query_id]
                ),
                "",
            ]
        )

    lines.extend(
        [
            "## Evidence brought together in the ISG",
            "",
            _markdown_table(evidence),
            "",
            "## Meaning supplied by the knowledge graph",
            "",
            "The unfamiliar column name `ApexOneSearches` is not just text. Through the "
            "data catalog and knowledge graph it is linked to an entity with wider meaning:",
            "",
            _markdown_table(kg_context),
            "",
            "## Filling the false negative",
            "",
            "No individual query says, \"ApexOne is taking our customers.\" The missing "
            "competitor is a false negative in the enterprise's current picture: an important "
            "entity and causal relationship have not yet been represented.",
            "",
            "Taken together, the retained insights form a much stronger hypothesis:",
            "",
            "1. Customers and revenue begin disappearing in the same narrow period.",
            "2. Spending per remaining customer stays stable.",
            "3. Marketing auction pressure rises while landing-page conversion stays stable.",
            "4. Searches for the previously insignificant name ApexOne jump sharply.",
            "5. Customers increasingly report switching to another provider.",
            "6. Price, service, product performance, and fulfillment remain stable.",
            "7. The knowledge graph identifies ApexOne as a newly funded competitor whose "
            "launch date and target segment align with the observed changes.",
            "",
            "This does not mathematically prove causation. It identifies a well-supported "
            "risk hypothesis that no one analyst was positioned to see: a heavily funded "
            "competitor entered quickly and began taking customers before normal word of "
            "mouth and organizational reporting could catch up.",
        ]
    )

    path = output_dir / "BLOG_EXAMPLE_ASSETS.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def run(output_dir: str | Path = "competitor_surprise_output", seed: int = 42) -> Path:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    queries = build_scenario(seed=seed)
    selected_by_query: dict[str, pd.DataFrame] = {}
    all_selected = []
    querydef_records = []

    for query in queries:
        data_path = destination / f"{query.query_id.lower().replace('-', '_')}_data.csv"
        query.dataframe.to_csv(data_path, index=False)

        detected = detect_visualization_insights(query.dataframe.copy())
        full_insights = insights_to_dataframe(detected)
        full_insights.to_csv(
            destination / f"{query.query_id.lower().replace('-', '_')}_all_insights.csv",
            index=False,
        )

        selected = _selected_insights(query, detected)
        selected.to_csv(
            destination / f"{query.query_id.lower().replace('-', '_')}_selected_insights.csv",
            index=False,
        )
        selected_by_query[query.query_id] = selected
        all_selected.append(selected)

        record = query.metadata()
        record["recommended_visualizations"] = detected.get(
            "recommended_visualizations", []
        )
        record["selected_insight_count"] = len(selected)
        querydef_records.append(record)

    nonempty_selected = [
        frame.dropna(axis=1, how="all")
        for frame in all_selected
        if not frame.empty
    ]
    consolidated = (
        pd.concat(nonempty_selected, ignore_index=True)
        if nonempty_selected
        else pd.DataFrame()
    )
    consolidated.to_csv(destination / "isg_selected_insights.csv", index=False)

    evidence = build_isg_evidence_table(consolidated)
    evidence.to_csv(destination / "isg_evidence.csv", index=False)

    kg_context = build_kg_context_table()
    kg_context.to_csv(destination / "kg_context.csv", index=False)

    (destination / "querydefs.json").write_text(
        json.dumps(querydef_records, indent=2), encoding="utf-8"
    )

    chart_files = _write_charts(queries, destination)
    return _write_blog_assets_markdown(
        queries,
        selected_by_query,
        chart_files,
        evidence,
        kg_context,
        destination,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the fictional cross-domain competitor-surprise example."
    )
    parser.add_argument(
        "--output",
        default="competitor_surprise_output",
        help="Directory to receive CSV, PNG, JSON, and Markdown assets.",
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    report = run(args.output, args.seed)
    print(f"Wrote scenario assets to: {report.parent.resolve()}")
    print(f"Markdown report: {report.resolve()}")


if __name__ == "__main__":
    main()
