from __future__ import annotations

from sqlalchemy import select

from app import models
from app.db import SessionLocal
from app.resolver import resolve_benchmarks


def test_resolver_handles_exact_alias(seeded_db) -> None:
    with SessionLocal() as session:
        benchmarks = list(session.scalars(select(models.Benchmark)))

    matches = resolve_benchmarks("BFCL", benchmarks)
    assert matches[0]["benchmark_id"] == "bfcl"
    assert matches[0]["confidence"] == 1.0


def test_resolver_handles_function_calling_query(seeded_db) -> None:
    with SessionLocal() as session:
        benchmarks = list(session.scalars(select(models.Benchmark)))

    matches = resolve_benchmarks("best benchmark for function calling", benchmarks)
    assert any(match["benchmark_id"] == "bfcl" for match in matches)

