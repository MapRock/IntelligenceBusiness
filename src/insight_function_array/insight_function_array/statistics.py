"""Reusable numeric helpers for insight analyzers."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .settings import CLUSTER_K_RANGE, SILHOUETTE_MIN

try:
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    SKLEARN_AVAILABLE = True
except ImportError:  # optional dependency
    KMeans = None
    silhouette_score = None
    SKLEARN_AVAILABLE = False


def robust_z(series: pd.Series) -> np.ndarray:
    """Return robust z-scores based on median absolute deviation.

    Falls back to an ordinary standard deviation when the MAD is degenerate.
    """
    values = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
    median = np.nanmedian(values)
    mad = np.nanmedian(np.abs(values - median))

    if not np.isfinite(mad) or mad == 0:
        std = np.nanstd(values)
        if not np.isfinite(std) or std == 0:
            return np.zeros_like(values)
        return (values - np.nanmean(values)) / std

    return 0.6745 * (values - median) / mad


def standardize(values: np.ndarray) -> np.ndarray:
    """Standardize each column while tolerating NaNs and constant columns."""
    mean = np.nanmean(values, axis=0)
    std = np.nanstd(values, axis=0)
    std[~np.isfinite(std) | (std == 0)] = 1.0
    return (values - mean) / std


def best_kmeans(values: np.ndarray, k_range=CLUSTER_K_RANGE):
    """Return ``(labels, silhouette_score, k)`` for the best accepted model.

    If scikit-learn is unavailable or no tested model clears the silhouette
    threshold, return ``(None, None, None)``.
    """
    if not SKLEARN_AVAILABLE:
        return None, None, None

    best_labels = None
    best_score = -1.0
    best_k = None

    for k in k_range:
        model = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = model.fit_predict(values)
        if len(np.unique(labels)) < 2:
            continue
        score = silhouette_score(values, labels)
        if score > best_score:
            best_labels, best_score, best_k = labels, score, k

    if best_labels is None or best_score < SILHOUETTE_MIN:
        return None, None, None
    return best_labels, best_score, best_k
