"""Convert the engine's stable dictionary result into tabular or text output."""

from __future__ import annotations

from collections import defaultdict
import re

import pandas as pd


def insights_to_dataframe(insights: dict) -> pd.DataFrame:
    recommended = set(insights.get("recommended_visualizations", []))
    findings = insights.get("findings", {}) or {}
    columns = [
        "key",
        "chart",
        "facet",
        "metric",
        "metric_x",
        "metric_y",
        "series_a",
        "series_b",
        "message",
        "tags",
        "score",
        "date_hint",
        "chart_recommended",
    ]
    rows = []

    for key, message in findings.items():
        chart, separator, facet = key.partition(" - ")
        chart = chart.strip() or None
        facet = facet.strip() if separator else None
        lower_message = (message or "").lower()
        row = {column: None for column in columns}
        row.update(
            key=key,
            chart=chart,
            facet=facet,
            message=message,
            chart_recommended=chart in recommended,
        )

        if facet:
            pair = re.match(r"(.+?)\s+vs\s+(.+)", facet, flags=re.I)
            if pair:
                row["metric_x"] = pair.group(1).strip()
                row["metric_y"] = pair.group(2).strip()

            intersection = re.match(r"(.+?)\s*∩\s*(.+)", facet)
            if intersection:
                row["series_a"] = intersection.group(1).strip()
                row["series_b"] = intersection.group(2).strip()

            if not row["metric_x"] and not row["series_a"]:
                row["metric"] = facet

        tags = []
        keyword_tags = {
            "correlation": "correlation",
            "cluster": "clusters",
            "trend": "trend",
            "spike": "spikes",
            "inflection": "inflection",
            "variance": "variance",
            "dominates": "dominance",
            "skew": "skewed",
            "discrete": "discrete",
            "dispersion": "dispersion",
            "stable": "stability",
        }
        for keyword, tag in keyword_tags.items():
            if keyword in lower_message:
                tags.append(tag)
        if "intersection" in lower_message or "∩" in (facet or ""):
            tags.append("intersections")
        row["tags"] = ",".join(dict.fromkeys(tags)) or None

        score = re.search(r"\((?:\s*silhouette\s*)?([\-+]?\d*\.?\d+)\)", lower_message)
        if score:
            try:
                row["score"] = float(score.group(1))
            except ValueError:
                pass

        date_hint = re.search(r"(\d{4}-\d{2}-\d{2})", message or "")
        if date_hint:
            row["date_hint"] = date_hint.group(1)

        rows.append(row)

    return pd.DataFrame(rows, columns=columns)


def recommendations_to_dataframe(insights: dict) -> pd.DataFrame:
    recommendations = insights.get("recommended_visualizations", []) or []
    return pd.DataFrame(
        {"rank": range(1, len(recommendations) + 1), "chart": recommendations}
    )


def _group_findings(findings: dict) -> dict:
    grouped = defaultdict(dict)
    for key, value in findings.items():
        chart, separator, facet = key.partition(" - ")
        grouped[chart.strip()][facet.strip() if separator else ""] = value
    return grouped


def insights_to_markdown(insights: dict) -> str:
    recommendations = insights.get("recommended_visualizations", [])
    findings = _group_findings(insights.get("findings", {}))
    output = []

    if recommendations:
        output.extend(
            ["### Recommended visualizations", " · ".join(recommendations), ""]
        )
    if findings:
        output.append("### Findings")
        for chart, facets in findings.items():
            output.append(f"- **{chart}**")
            for facet, message in facets.items():
                label = f"*{facet}*: " if facet else ""
                output.append(f"  - {label}{message}")
    return "\n".join(output)
