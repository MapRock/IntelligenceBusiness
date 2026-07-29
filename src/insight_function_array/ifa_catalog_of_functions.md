# Insight Function Array: Current and Missing Insight Functions

## Current Insight Functions

The table below lists methods decorated with `@insight` in the current analyzer code.

| Analyzer file | Visualization type | Function name | Description | Function output type |
|---|---|---|---|---|
| `analyzers/bar.py` | Bar Chart | `_dominant_category` | Detects whether the largest category accounts for at least the configured share of the aggregated metric. The current default threshold is 35%. | `str \| None` — a ready-to-store finding message or no finding |
| `analyzers/bar.py` | Bar Chart | `_high_dispersion` | Detects large differences among category bars using coefficient of variation, with a secondary standard-deviation-to-maximum test. | `str \| None` — a ready-to-store finding message or no finding |
| `analyzers/histogram.py` | Histogram | `_skew_finding` | Detects a substantially skewed numeric distribution. The current test is absolute skewness greater than 1. | `str \| None` — a ready-to-store finding message or no finding |
| `analyzers/histogram.py` | Histogram | `_discrete_finding` | Detects a numeric column with relatively few distinct values. The current test is fewer than 10 distinct non-null values. | `str \| None` — a ready-to-store finding message or no finding |
| `analyzers/line.py` | Line Chart | `_detect_strong_trend` | Detects a strong sustained direction by comparing the mean first difference with the baseline standard deviation. | `bool` — `analyze()` converts `True` into a finding message |
| `analyzers/line.py` | Line Chart | `_detect_spikes` | Detects sudden changes by applying a robust z-score to first differences. The current threshold is an absolute robust z-score of at least 3. | `list[index value]`, normally `list[pd.Timestamp]` — `analyze()` reports the count and first date |
| `analyzers/line.py` | Line Chart | `_detect_inflection` | Detects a sustained level change around a possible breakpoint using before/after windows, baseline standard deviation, and a same-direction run. | Index value or `None`, normally `pd.Timestamp \| None` — `analyze()` creates the finding message |
| `analyzers/line.py` | Line Chart | `_stable_finding` | Detects a numeric series that remains within a narrow band. It provides negative evidence that a suspected price, quality, service, or operating measure did not materially change. | `str \| None` — a ready-to-store finding message or no finding |
| `analyzers/line.py` | Line Chart | `_detect_intersections` | Detects crossings between comparable wide-form numeric series, such as `Sales_A` and `Sales_B`. It avoids comparing unrelated measures by checking their name families. | `list[tuple[str, str, int, index value]]` — series names, crossing count, and first crossing time |
| `analyzers/scatter.py` | Scatter Plot | `_correlation_finding` | Detects a strong linear relationship between two numeric variables. The current threshold is absolute Pearson correlation greater than 0.7. | `str \| None` — a ready-to-store finding message or no finding |
| `analyzers/scatter.py` | Scatter Plot | `_cluster_finding` | Detects distinct groups using K-means in either two-dimensional or higher-dimensional numeric space. It tries 2 through 5 clusters and retains a result only when the silhouette score meets the configured threshold. | `str \| None` — a ready-to-store finding message or no finding |
| `analyzers/pie.py` | Pie Chart | — | The pie-chart analyzer currently determines applicability and renders the chart, but it contains no insight-detection function. | No insight output |

## Current Output Pattern

The code currently uses two different output patterns:

| Pattern | Functions |
|---|---|
| Returns a finished human-readable finding | `_dominant_category`, `_high_dispersion`, `_skew_finding`, `_discrete_finding`, `_stable_finding`, `_correlation_finding`, `_cluster_finding` |
| Returns a raw detection result that `analyze()` converts into text | `_detect_strong_trend`, `_detect_spikes`, `_detect_inflection`, `_detect_intersections` |

For eventual ISG storage, these could be normalized into a structured `Insight` result containing the insight type, columns, values, score, threshold, time range, and human-readable message.

## Examples of Insight Functions Not Currently Implemented

These are examples suggested by the visualizations and the current architecture. They are not present in the reviewed code.

| Analyzer or proposed analyzer | Visualization type | Example missing insight | What it would detect | Suggested output type |
|---|---|---|---|---|
| `analyzers/line.py` | Line Chart | Trend direction and magnitude | Whether the series is rising or falling, its slope, and the strength of the movement. The current trend function only returns a Boolean. | Structured trend result: direction, slope, normalized strength, start and end |
| `analyzers/line.py` | Line Chart | Seasonality or periodicity | Repeating weekly, monthly, quarterly, annual, or other cycles. | List of detected periods with strength and phase |
| `analyzers/line.py` | Line Chart | Acceleration or deceleration | Whether the rate of increase or decrease is itself changing. | Direction, first slope, later slope, acceleration score |
| `analyzers/line.py` | Line Chart | Volatility change | A transition from stable to erratic behavior, or the reverse. | Before/after volatility, change ratio, breakpoint |
| `analyzers/line.py` | Line Chart | Local peaks and troughs | Meaningful high and low turning points rather than isolated spikes. | List of peak/trough dates, values, and prominence |
| `analyzers/line.py` | Line Chart | Missing periods or gaps | Missing dates, unexpected reporting gaps, or irregular time intervals. | List of missing intervals and expected frequency |
| `analyzers/line.py` | Line Chart | Plateau after growth or decline | A series that rises or falls and then becomes stable. | Prior trend, plateau start, plateau level |
| `analyzers/line.py` | Line Chart | Divergence or convergence | Two comparable series moving farther apart or closer together without necessarily crossing. | Series pair, direction, rate, start/end separation |
| `analyzers/bar.py` | Bar Chart | Top-N concentration | How much of the total is held by the top 3, 5, or other number of categories. | Top-N share and category list |
| `analyzers/bar.py` | Bar Chart | Runner-up gap | Whether the leading category is only slightly ahead or far ahead of the second category. | First and second category, values, absolute and relative gap |
| `analyzers/bar.py` | Bar Chart | Long tail | A few large categories followed by many very small categories. | Head share, tail count, tail share |
| `analyzers/bar.py` | Bar Chart | Near equality | Categories with unusually similar values, suggesting no meaningful leader. | Dispersion score and equal-share group |
| `analyzers/bar.py` | Bar Chart | Category outlier | One category that is unusually high or low relative to its peers even when it does not dominate the total. | Category, value, peer baseline, z-score or robust score |
| `analyzers/bar.py` | Bar Chart | Sign split | A mix of positive and negative categories, such as gains and losses. | Positive categories, negative categories, net value |
| `analyzers/histogram.py` | Histogram | Multimodality | Two or more peaks suggesting distinct populations or operating modes. | Number and approximate location of modes |
| `analyzers/histogram.py` | Histogram | Extreme outliers | Values far beyond the central distribution. | Outlier rows or values with robust scores |
| `analyzers/histogram.py` | Histogram | Zero inflation | An unusually large share of zeros compared with the rest of the distribution. | Zero count, zero share, nonzero distribution summary |
| `analyzers/histogram.py` | Histogram | Heavy tails or high kurtosis | More extreme values than expected from a bell-shaped distribution. | Kurtosis, tail counts, tail thresholds |
| `analyzers/histogram.py` | Histogram | Narrow concentration | Most values compressed into a very small range. | Central interval, included share, overall range |
| `analyzers/histogram.py` | Histogram | Distribution gaps | Empty or sparse ranges between populated parts of the distribution. | Gap boundaries and counts on each side |
| `analyzers/scatter.py` | Scatter Plot | Point outliers | Individual points far from the main relationship or clusters. | Row identifiers, coordinates, outlier score |
| `analyzers/scatter.py` | Scatter Plot | Nonlinear relationship | Curved, threshold, exponential, or other non-linear association missed by Pearson correlation. | Relationship type, nonlinear score, fitted parameters |
| `analyzers/scatter.py` | Scatter Plot | Heteroscedasticity | Increasing or decreasing spread of one variable as the other changes. | Direction and magnitude of variance change |
| `analyzers/scatter.py` | Scatter Plot | Subgroup separation | Categories occupying visibly different regions of the scatter plot. | Category pairs, separation score, centroids |
| `analyzers/scatter.py` | Scatter Plot | Correlation by subgroup | A relationship that is strong in one category but weak or reversed in another. | Correlation per group and difference among groups |
| `analyzers/scatter.py` | Scatter Plot | Quadrant concentration | A disproportionate number of observations in one high/low combination. | Quadrant counts, shares, and dominant quadrant |
| `analyzers/pie.py` | Pie Chart | Dominant slice | One category holding an unusually large share. | Category, share, threshold |
| `analyzers/pie.py` | Pie Chart | Composition concentration | Whether the composition is concentrated in a few slices or spread broadly. | HHI, entropy, or top-N share |
| `analyzers/pie.py` | Pie Chart | Fragmentation | Many small slices with no clear leader. | Slice count, largest share, small-slice share |
| `analyzers/pie.py` | Pie Chart | Near-equal shares | Most categories contributing approximately the same proportion. | Equality score and share range |
| `analyzers/pie.py` | Pie Chart | Small-slice long tail | A collection of tiny categories that may be better grouped as “Other.” | Small-slice count, combined share, category list |
| Proposed `box.py` | Box Plot | Group median difference | Material differences in medians across categories. | Group medians, largest gap, effect size |
| Proposed `box.py` | Box Plot | Group spread difference | One group having much greater variability than others. | IQR or variance per group and spread ratio |
| Proposed `box.py` | Box Plot | Group-specific outliers | Outliers occurring within particular categories. | Group, row or value, outlier score |
| Proposed `heatmap.py` | Heat Map | Hotspot or cold spot | Cells or regions materially higher or lower than surrounding cells. | Coordinates, value, local baseline, score |
| Proposed `heatmap.py` | Heat Map | Row or column band | A whole row, column, period, or category behaving unusually. | Row/column identifier and deviation score |
| Proposed `stacked_area.py` | Stacked Area Chart | Composition shift over time | One category gaining share while another loses share. | Category pair, share changes, change period |
| Proposed `funnel.py` | Funnel Chart | Stage drop-off | An unexpectedly large loss between two process stages. | From-stage, to-stage, loss count and rate |
| Proposed `map.py` | Geographic Map | Geographic cluster or hotspot | Spatial concentration of unusually high or low values. | Region or coordinates, spatial score, neighboring areas |
| Proposed `table.py` | Highlight Table / Crosstab | Exceptional cell | A value unusually high or low for its row, column, or peer group. | Row key, column key, value, expected value, deviation |
| Proposed `table.py` | Highlight Table / Crosstab | Rank reversal | A category whose rank changes materially between periods or groups. | Old rank, new rank, change magnitude |


