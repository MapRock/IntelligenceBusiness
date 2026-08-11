"""Inspect the analyzer registry as a catalog of visualization insight functions."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import inspect

import pandas as pd

from .registry import get_analyzers


@dataclass(frozen=True)
class InsightFunctionMetadata:
    visualization: str
    analyzer_class: str
    function_name: str
    what: str
    value: str


def get_insight_function_catalog() -> list[InsightFunctionMetadata]:
    """Return one record for every method decorated with ``@insight``."""
    records = []
    for analyzer in get_analyzers():
        analyzer_class = type(analyzer)
        for function_name, function in inspect.getmembers(analyzer_class, inspect.isfunction):
            if not getattr(function, "_is_insight", False):
                continue
            records.append(
                InsightFunctionMetadata(
                    visualization=analyzer.chart_name,
                    analyzer_class=analyzer_class.__name__,
                    function_name=function_name,
                    what=getattr(function, "what", ""),
                    value=getattr(function, "value", ""),
                )
            )
    return sorted(records, key=lambda item: (item.visualization, item.function_name))


def insight_function_catalog_dataframe() -> pd.DataFrame:
    """Return the insight-function catalog in a KG/export-friendly table."""
    return pd.DataFrame(asdict(record) for record in get_insight_function_catalog())
