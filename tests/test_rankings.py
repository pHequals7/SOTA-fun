from __future__ import annotations

from app.db import SessionLocal
from app.rankings import top_for_benchmark


def test_top_for_benchmark_returns_ranked_seed_result(seeded_db) -> None:
    with SessionLocal() as session:
        result = top_for_benchmark(session, benchmark_id="swe_bench_verified", k=3)

    assert result["benchmark"]["id"] == "swe_bench_verified"
    assert len(result["results"]) >= 2
    assert result["results"][0]["rank"] == 1
    assert result["results"][0]["score"] >= result["results"][1]["score"]
    assert any(row["model_id"] == "claude_opus_4_7" for row in result["results"])


def test_best_available_includes_mode_warning(seeded_db) -> None:
    with SessionLocal() as session:
        result = top_for_benchmark(
            session, benchmark_id="swe_bench_verified", k=3, mode="best_available"
        )

    assert result["warnings"]
