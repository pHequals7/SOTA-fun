from __future__ import annotations

from app.registry import load_benchmarks, load_labs, load_seed_data
from app.schemas import BenchmarkRead, LabRead, ModelRead, ScoreRead


def test_registry_rows_validate_against_schemas() -> None:
    for lab in load_labs():
        LabRead.model_validate(lab)
    for benchmark in load_benchmarks():
        BenchmarkRead.model_validate(benchmark)
    for model in load_seed_data()["models"]:
        ModelRead.model_validate(model)


def test_seed_score_schema_accepts_expected_enums(seeded_db) -> None:
    from sqlalchemy import select

    from app import models
    from app.db import SessionLocal

    with SessionLocal() as session:
        row = session.scalars(select(models.ReportedBenchmarkScore)).first()
        assert row is not None
        score = ScoreRead.model_validate(row)
        assert score.verification_status == "unverified"

