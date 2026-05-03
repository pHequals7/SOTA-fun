from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.schemas import ExtractionMethod, ScoreUnit, VerificationStatus


def _parse_date(value: Any) -> date | None:
    if value is None or isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def validate_score_payload(payload: dict[str, Any], session: Session) -> list[str]:
    errors: list[str] = []

    if not session.get(models.Benchmark, payload.get("benchmark_id")):
        errors.append("benchmark_id does not exist in registry")

    model_id = payload.get("model_id")
    if not model_id:
        errors.append("model_id is required")

    try:
        float(payload.get("score"))
    except (TypeError, ValueError):
        errors.append("score must be numeric")

    if payload.get("higher_is_better") is None:
        errors.append("higher_is_better is required")

    if not payload.get("source_url"):
        errors.append("source_url is required")

    if payload.get("extraction_method") not in set(ExtractionMethod):
        errors.append("extraction_method is invalid")

    confidence = payload.get("confidence")
    if confidence is None or not 0 <= float(confidence) <= 1:
        errors.append("confidence must be between 0 and 1")

    if not _parse_date(payload.get("snapshot_week")):
        errors.append("snapshot_week must be a valid ISO date")

    if payload.get("score_unit") not in set(ScoreUnit):
        errors.append("score_unit is invalid")

    if payload.get("verification_status") not in set(VerificationStatus):
        errors.append("verification_status is invalid")

    return errors


def score_exists(session: Session, payload: dict[str, Any]) -> bool:
    stmt = select(models.ReportedBenchmarkScore.id).where(
        models.ReportedBenchmarkScore.model_id == payload["model_id"],
        models.ReportedBenchmarkScore.benchmark_id == payload["benchmark_id"],
        models.ReportedBenchmarkScore.snapshot_week == _parse_date(payload["snapshot_week"]),
        models.ReportedBenchmarkScore.score == float(payload["score"]),
        models.ReportedBenchmarkScore.source_url == payload["source_url"],
    )
    return session.execute(stmt).first() is not None

