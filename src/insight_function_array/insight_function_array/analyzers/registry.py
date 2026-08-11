"""Discover analyzer plug-ins from the built-in analyzers package."""

from __future__ import annotations

import importlib
import inspect
import pkgutil

from . import analyzers as analyzers_package
from .analyzers.base import ChartAnalyzer


def get_analyzers() -> list[ChartAnalyzer]:
    """Instantiate all concrete ``ChartAnalyzer`` subclasses.

    Discovery remains dynamic, like the October 2025 ``viz_registry.py``, but
    is restricted to the package's analyzer namespace and sorted for stable
    results.
    """
    analyzer_classes: dict[str, type[ChartAnalyzer]] = {}

    for module_info in pkgutil.iter_modules(
        analyzers_package.__path__,
        analyzers_package.__name__ + ".",
    ):
        if module_info.name.endswith(".base"):
            continue
        module = importlib.import_module(module_info.name)
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if (
                cls is not ChartAnalyzer
                and issubclass(cls, ChartAnalyzer)
                and cls.__module__ == module.__name__
            ):
                analyzer_classes[cls.__name__] = cls

    return [analyzer_classes[name]() for name in sorted(analyzer_classes)]
