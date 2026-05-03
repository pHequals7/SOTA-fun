from __future__ import annotations

from scripts.export_snapshot import export_snapshot


def test_export_snapshot_writes_required_files(seeded_db) -> None:
    path = export_snapshot()
    latest = path.parent / "latest"

    assert (latest / "benchmark_scores.csv").exists()
    assert (latest / "benchmark_scores.parquet").exists()
    assert (latest / "models.csv").exists()
    assert (latest / "benchmarks.csv").exists()
    assert (latest / "sources.csv").exists()

