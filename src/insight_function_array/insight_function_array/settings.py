"""Central thresholds used by the simple insight functions.

These values are the October 2025 defaults, collected in one place so the
engine can eventually support per-domain or per-visualization tuning.
"""

CLUSTER_K_RANGE = range(2, 6)
SILHOUETTE_MIN = 0.35
SPIKE_Z = 3.0
INFLECT_WINDOW = 3
INFLECT_SIGMA = 1.0
SUSTAINED_MIN_RUN = 3
DOMINANCE_MIN_SHARE = 0.35

# Defaults used by the bar-chart dispersion detector. The original analyzer
# accessed these through getattr with the same fallback values.
BAR_HIGH_CV = 0.50
BAR_STD_REL_MAX = 0.50

# Stability detector defaults.
STABILITY_MAX_CV = 0.03
STABILITY_MAX_RELATIVE_CHANGE = 0.05
STABILITY_MIN_POINTS = 6
