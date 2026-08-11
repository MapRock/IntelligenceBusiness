"""Infer dataframe roles used when selecting compatible visualizations."""

from __future__ import annotations

import pandas as pd


def infer_columns(
    df: pd.DataFrame,
    auto_categorical_max_unique: int = 20,
) -> tuple[list[str], list[str], str | None]:
    """Infer categorical, numerical, and time columns.

    Numeric low-cardinality columns remain numerical but may also serve as
    categorical grouping columns. Date/time columns are explicitly excluded
    from the numerical and categorical lists.
    """
    time_col = next(
        (
            col
            for col in df.columns
            if any(
                token in str(col).lower()
                for token in (
                    "date", "time", "timestamp", "datetime",
                    "week", "month", "quarter", "year", "period",
                )
            )
        ),
        None,
    )

    if time_col and not pd.api.types.is_datetime64_any_dtype(df[time_col]):
        try:
            converted = pd.to_datetime(df[time_col], errors="coerce")
            if converted.notna().any():
                df[time_col] = converted
        except (TypeError, ValueError):
            pass

    numerical_cols = [
        col
        for col in df.select_dtypes(include=["number"]).columns.tolist()
        if not pd.api.types.is_datetime64_any_dtype(df[col])
        and not pd.api.types.is_timedelta64_dtype(df[col])
        and col != time_col
    ]
    object_cats = [
        col
        for col in df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
        if col != time_col
    ]

    row_count = len(df)
    max_unique = min(auto_categorical_max_unique, max(5, row_count // 50))
    low_card_nums = [
        col
        for col in numerical_cols
        if df[col].nunique(dropna=True) <= max_unique
    ]
    categorical_cols = list(dict.fromkeys(object_cats + low_card_nums))

    return categorical_cols, numerical_cols, time_col
