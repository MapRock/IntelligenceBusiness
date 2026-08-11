"""Synthetic dataframes that exercise individual insight functions."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def line_trend(seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start="2022-01-01", periods=12, freq="D")
    sales = np.linspace(100, 600, len(dates)) + rng.normal(0, 10, len(dates))
    profit = 0.5 * sales + rng.normal(0, 5, len(dates))
    quantity = np.linspace(3, 10, len(dates)) + rng.normal(0, 0.3, len(dates))
    return pd.DataFrame(
        {
            "Date": dates,
            "Sales": np.round(sales, 2),
            "Profit": np.round(profit, 2),
            "Quantity": np.round(quantity).astype(int),
        }
    )


def line_spikes(seed: int = 9) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start="2022-02-01", periods=60, freq="D")
    sales = 200 + rng.normal(0, 5, len(dates))
    positions = rng.choice(len(dates), size=4, replace=False)
    sales[positions] += rng.choice([120, -100, 150, -130], size=4, replace=True)
    profit = 0.4 * sales + rng.normal(0, 10, len(dates))
    return pd.DataFrame({"Date": dates, "Sales": sales.round(2), "Profit": profit.round(2)})


def line_inflection(seed: int = 11) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start="2022-03-01", periods=60, freq="D")
    sales = np.concatenate([150 + rng.normal(0, 6, 30), 280 + rng.normal(0, 6, 30)])
    profit = 0.45 * sales + rng.normal(0, 8, len(dates))
    return pd.DataFrame({"Date": dates, "Sales": sales.round(2), "Profit": profit.round(2)})


def scatter_corr_clusters(seed: int = 101, count: int = 500) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    sales = rng.normal(500, 80, count)
    profit = 0.55 * sales - 50 + rng.normal(0, 30, count)
    centers = np.array([[0, 0], [4, 5], [-5, 3]])
    labels = rng.integers(0, len(centers), count)
    coordinates = centers[labels] + rng.normal(0, 0.7, (count, 2))
    return pd.DataFrame(
        {
            "X": coordinates[:, 0].round(3),
            "Y": coordinates[:, 1].round(3),
            "Sales": sales.round(2),
            "Profit": profit.round(2),
            "ClusterLabel": labels,
        }
    )


def save_csv(dataframe: pd.DataFrame, path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(destination, index=False)
    return destination.resolve()
