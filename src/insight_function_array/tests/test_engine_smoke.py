from insight_function_array import detect_visualization_insights, insights_to_dataframe
from insight_function_array.demo.datasets import line_inflection, scatter_corr_clusters
from insight_function_array.registry import get_analyzers


def test_registry_discovers_uploaded_analyzers():
    names = {analyzer.chart_name for analyzer in get_analyzers()}
    assert names == {"Bar Chart", "Histogram", "Line Chart", "Pie Chart", "Scatter Plot"}


def test_line_dataset_produces_line_findings():
    result = detect_visualization_insights(line_inflection())
    assert "Line Chart" in result["recommended_visualizations"]
    assert any(key.startswith("Line Chart -") for key in result["findings"])


def test_scatter_dataset_produces_scatter_findings():
    result = detect_visualization_insights(scatter_corr_clusters())
    assert "Scatter Plot" in result["recommended_visualizations"]
    assert any(key.startswith("Scatter Plot -") for key in result["findings"])
    assert not insights_to_dataframe(result).empty


def test_insight_metadata_catalog_is_discoverable():
    from insight_function_array import get_insight_function_catalog

    records = get_insight_function_catalog()
    names = {(record.visualization, record.function_name) for record in records}
    assert ("Bar Chart", "_dominant_category") in names
    assert ("Line Chart", "_detect_spikes") in names
    assert ("Scatter Plot", "_correlation_finding") in names
