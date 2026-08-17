"""Line-chart applicability, insight functions, and rendering."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import re
import pandas as pd

from ..settings import (
    INFLECT_SIGMA,
    INFLECT_WINDOW,
    SPIKE_Z,
    STABILITY_MAX_CV,
    STABILITY_MAX_RELATIVE_CHANGE,
    STABILITY_MIN_POINTS,
    SUSTAINED_MIN_RUN,
)
from ..statistics import robust_z
from .base import ChartAnalyzer, insight


def _date_label(value) -> str:
    return value.date().isoformat() if hasattr(value, "date") else str(value)


def _series_family(column_name: str) -> str:
    """Return a conservative family name for comparable wide-form series.

    Examples: ``Sales_A`` and ``Sales_B`` share the ``sales`` family.
    Unrelated measures such as ``UptimePct`` and ``PriceIndex`` do not.
    """
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", str(column_name)).strip("_")
    parts = normalized.split("_")
    if len(parts) >= 2 and len(parts[-1]) <= 3:
        return "_".join(parts[:-1]).lower()
    match = re.match(r"(.+?)(?:[A-Z]|\d+)$", str(column_name))
    if match and "_" in str(column_name):
        return match.group(1).rstrip("_").lower()
    return normalized.lower()


class LineChartAnalyzer(ChartAnalyzer):
    chart_name = "Line Chart"

    def is_applicable(self, df, categorical_cols, numerical_cols, time_col):
        return time_col is not None and len(numerical_cols) >= 1

    @insight(
        what="A strong sustained direction in a time series.",
        value="A trend may indicate growth, decline, or a developing condition.",
    )
    def _detect_strong_trend(self, ts: pd.Series, baseline_std: float) -> bool:
        trend = ts.diff().mean()
        return pd.notna(trend) and pd.notna(baseline_std) and abs(trend) > 0.5 * baseline_std

    @insight(
        what="Sudden large changes in time-series data that deviate significantly from the norm.",
        value="A spike may indicate an anomaly or significant occurrence.",
    )
    def _detect_spikes(self, ts: pd.Series):
        differences = ts.diff().dropna()
        if differences.empty:
            return []
        z_scores = robust_z(differences)
        positions = np.where(np.abs(z_scores) >= SPIKE_Z)[0]
        return list(differences.index[positions])

    @insight(
        what="A sustained level change around a possible breakpoint.",
        value="An inflection can indicate a regime, policy, process, or environmental change.",
    )
    def _detect_inflection(self, ts: pd.Series, baseline_std: float):
        window = max(1, int(INFLECT_WINDOW))
        if ts.size < 2 * window + 2 or not np.isfinite(baseline_std) or baseline_std == 0:
            return None

        values = ts.to_numpy(dtype=float)
        best_position = None
        best_delta = 0.0

        for position in range(window, len(values) - window - 1):
            before = np.nanmean(values[position - window : position])
            after = np.nanmean(values[position + 1 : position + 1 + window])
            delta = after - before
            post_signs = np.sign(
                np.diff(values[position : position + 1 + SUSTAINED_MIN_RUN])
            )
            sustained = (
                len(post_signs) == SUSTAINED_MIN_RUN
                and np.all(post_signs == np.sign(delta))
            )
            if (
                np.isfinite(delta)
                and abs(delta) > INFLECT_SIGMA * baseline_std
                and sustained
                and abs(delta) > best_delta
            ):
                best_position = position
                best_delta = abs(delta)

        return None if best_position is None else ts.index[best_position]


    @insight(
        what="A numeric series remains within a narrow band over time.",
        value=(
            "Stability is useful negative evidence: it can help rule out a suspected "
            "price, quality, service, or operating change."
        ),
    )
    def _stable_finding(self, ts: pd.Series, num_col: str) -> str | None:
        clean = pd.to_numeric(ts, errors="coerce").dropna()
        if len(clean) < STABILITY_MIN_POINTS:
            return None

        mean_value = clean.mean()
        if not np.isfinite(mean_value) or mean_value == 0:
            return None

        cv = clean.std() / abs(mean_value)
        relative_change = abs(clean.iloc[-1] - clean.iloc[0]) / abs(mean_value)
        if cv <= STABILITY_MAX_CV and relative_change <= STABILITY_MAX_RELATIVE_CHANGE:
            return (
                f"Stable level detected in {num_col} "
                f"(CV≈{cv:.1%}; start-to-end change≈{relative_change:.1%})."
            )
        return None

    @insight(
        what="Two numeric series cross one another over time.",
        value="A crossing can indicate a reversal in rank or relative performance.",
    )
    def _detect_intersections(self, df, time_col, numerical_cols, max_pairs=3):
        if len(numerical_cols) < 2:
            return []

        pairs = []
        tried = 0
        for index, first in enumerate(numerical_cols):
            for second in numerical_cols[index + 1 :]:
                if _series_family(first) != _series_family(second):
                    continue
                tried += 1
                if tried > max_pairs:
                    return pairs

                grouped = (
                    df[[time_col, first, second]]
                    .dropna()
                    .groupby(time_col)[[first, second]]
                    .sum()
                    .sort_index()
                )
                if len(grouped) < 2:
                    continue

                sign = np.sign((grouped[first] - grouped[second]).to_numpy())
                for position in range(1, len(sign)):
                    if sign[position] == 0:
                        sign[position] = sign[position - 1]
                changes = np.where(sign[1:] * sign[:-1] < 0)[0]
                if len(changes):
                    first_crossing = grouped.index[changes[0] + 1]
                    pairs.append((first, second, len(changes), first_crossing))
        return pairs

    def analyze(self, df, categorical_cols, numerical_cols, time_col, add_finding):
        if not time_col:
            return

        for num_col in numerical_cols:
            ts = df.groupby(time_col, as_index=True)[num_col].sum().sort_index()
            if ts.size < 3:
                continue
            baseline_std = df[num_col].std()

            stable_message = self._stable_finding(ts, num_col)
            if stable_message:
                add_finding(self.chart_name, num_col, stable_message)
                continue

            if self._detect_strong_trend(ts, baseline_std):
                add_finding(
                    self.chart_name,
                    num_col,
                    f"Strong trend detected in {num_col} over {time_col}.",
                )

            spikes = self._detect_spikes(ts)
            if spikes:
                add_finding(
                    self.chart_name,
                    num_col,
                    f"{len(spikes)} spike(s) detected on {_date_label(spikes[0])}.",
                )

            inflection = self._detect_inflection(ts, baseline_std)
            if inflection is not None:
                add_finding(
                    self.chart_name,
                    num_col,
                    f"Inflection around {_date_label(inflection)} (sustained change).",
                )

        for first, second, count, when in self._detect_intersections(
            df, time_col, numerical_cols, max_pairs=3
        ):
            add_finding(
                self.chart_name,
                f"{first} ∩ {second}",
                f"{count} intersection(s), first at {_date_label(when)}.",
            )

    def plot(self, df, categorical_cols, numerical_cols, time_col, **kwargs):
        if not time_col:
            return None

        aggregation = kwargs.get("agg", "sum")
        if aggregation not in {"sum", "mean"}:
            aggregation = "sum"

        num_cols = kwargs.get("num_cols")
        num_col = kwargs.get("num_col") or (numerical_cols[0] if numerical_cols else None)
        hue = kwargs.get("hue")
        top_n = int(kwargs.get("top_n", 6))
        mark_intersections = bool(kwargs.get("mark_intersections", False))
        ax = plt.gca()

        def clean_numeric(frame, cols):
            result = frame.copy()
            for col in cols:
                result[col] = pd.to_numeric(result[col], errors="coerce").replace(
                    [np.inf, -np.inf], np.nan
                )
            return result

        if num_cols and len(num_cols) >= 2:
            grouped = (
                clean_numeric(df[[time_col] + list(num_cols)], num_cols)
                .groupby(time_col)
                .agg(aggregation)
                .sort_index()
            )
            for col in num_cols:
                ax.plot(grouped.index, grouped[col], label=str(col))

            if mark_intersections:
                for index, first in enumerate(num_cols):
                    for second in num_cols[index + 1 :]:
                        sign = np.sign((grouped[first] - grouped[second]).to_numpy())
                        for position in range(1, len(sign)):
                            if sign[position] == 0:
                                sign[position] = sign[position - 1]
                        changes = np.where(sign[1:] * sign[:-1] < 0)[0]
                        if len(changes):
                            point = grouped.index[changes[0] + 1]
                            y_value = grouped.loc[point, [first, second]].mean()
                            ax.axvline(point, linestyle="--", alpha=0.4)
                            ax.scatter([point], [y_value], s=30)

            ax.set_title(f"{aggregation.capitalize()} over time (multi-series)")
            ax.set_xlabel(str(time_col))
            ax.set_ylabel(aggregation.capitalize())
            ax.legend(title="Series", bbox_to_anchor=(1.02, 1), loc="upper left")
            return ax

        if hue and num_col:
            grouped = (
                clean_numeric(df[[time_col, hue, num_col]], [num_col])
                .dropna(subset=[num_col])
                .groupby([time_col, hue])[num_col]
                .agg(aggregation)
                .reset_index()
            )
            top_groups = grouped.groupby(hue)[num_col].sum().nlargest(top_n).index
            pivot = (
                grouped[grouped[hue].isin(top_groups)]
                .pivot(index=time_col, columns=hue, values=num_col)
                .sort_index()
            )
            for col in pivot.columns:
                ax.plot(pivot.index, pivot[col], label=str(col))
            ax.set_title(f"{num_col} by {hue} over time ({aggregation})")
            ax.set_xlabel(str(time_col))
            ax.set_ylabel(str(num_col))
            ax.legend(title=str(hue), bbox_to_anchor=(1.02, 1), loc="upper left")
            return ax

        if not num_col:
            return None
        series = (
            clean_numeric(df[[time_col, num_col]], [num_col])
            .groupby(time_col)[num_col]
            .agg(aggregation)
            .sort_index()
        )
        ax.plot(series.index, series.values)
        ax.set_title(f"{num_col} over {time_col} ({aggregation})")
        ax.set_xlabel(str(time_col))
        ax.set_ylabel(str(num_col))
        return ax
