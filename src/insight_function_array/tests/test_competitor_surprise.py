from insight_function_array.demo.competitor_surprise import build_scenario, run


def test_scenario_contains_cross_domain_queries():
    queries = build_scenario()
    assert [q.query_id for q in queries] == [
        "QD-SALES-001",
        "QD-MKT-001",
        "QD-CS-001",
        "QD-OPS-001",
    ]


def test_scenario_writes_blog_assets(tmp_path):
    report = run(tmp_path)
    assert report.exists()
    assert (tmp_path / "isg_evidence.csv").exists()
    assert (tmp_path / "kg_context.csv").exists()
    assert (tmp_path / "qd_sales_001.png").exists()
    assert (tmp_path / "qd_mkt_001_acquisition.png").exists()
    assert (tmp_path / "qd_cs_001.png").exists()
    assert (tmp_path / "qd_ops_001.png").exists()
