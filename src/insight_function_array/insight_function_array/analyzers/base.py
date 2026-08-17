"""Base protocol and metadata decorator for chart analyzers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable

import pandas as pd


class ChartAnalyzer(ABC):
    """A visualization-specific collection of simple insight functions."""

    chart_name = "Base"

    @abstractmethod
    def is_applicable(
        self,
        df: pd.DataFrame,
        categorical_cols: list[str],
        numerical_cols: list[str],
        time_col: str | None,
    ) -> bool:
        """Return whether this visualization is suitable for the dataframe."""

    @abstractmethod
    def analyze(
        self,
        df: pd.DataFrame,
        categorical_cols: list[str],
        numerical_cols: list[str],
        time_col: str | None,
        add_finding: Callable[[str, str, str | None], None],
    ) -> None:
        """Run the visualization's insight functions."""

    @abstractmethod
    def plot(
        self,
        df: pd.DataFrame,
        categorical_cols: list[str],
        numerical_cols: list[str],
        time_col: str | None,
        **kwargs,
    ):
        """Render the visualization and return a Matplotlib axes object."""


def insight(*, what: str = "", value: str = ""):
    """Attach human-readable purpose metadata to an insight function."""

    def decorate(function):
        function.what = what
        function.value = value
        function._is_insight = True
        return function

    return decorate
