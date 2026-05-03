from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app import models
from app.registry import load_seed_data
from app.validation import score_exists, validate_score_payload
from connectors.base import SourceConnector


class ManualSeedConnector(SourceConnector):
    source_id = "manual_seed"

    def discover(self) -> list[dict[str, Any]]:
        return [{"source": "registry/seed_data.yaml"}]

    def fetch_raw(self) -> list[dict[str, Any]]:
        return [load_seed_data()]

    def extract(self, raw_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        extracted: list[dict[str, Any]] = []
        for item in raw_items:
            extracted.extend(item.get("scores", []))
        return extracted

    def normalize(self, extracted_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return extracted_items

    def validate(self, normalized_items: list[dict[str, Any]]) -> dict[str, Any]:
        return {"count": len(normalized_items), "errors": []}

    def _coerce_dates(self, row: dict[str, Any]) -> dict[str, Any]:
        coerced = dict(row)
        date_keys = {"release_date", "model_release_date", "snapshot_week", "published_at", "source_published_at"}
        datetime_keys = {"fetched_at", "extracted_at", "last_seen_at", "created_at", "reviewed_at"}
        for key, value in list(coerced.items()):
            if value is None:
                continue
            if key in datetime_keys:
                if isinstance(value, datetime):
                    continue
                coerced[key] = datetime.fromisoformat(str(value))
            elif key in date_keys:
                if isinstance(value, date):
                    continue
                coerced[key] = date.fromisoformat(str(value))
        if "last_seen_at" in coerced and coerced["last_seen_at"] is None:
            coerced["last_seen_at"] = datetime.now(timezone.utc)
        return coerced

    def seed(self, session: Session) -> dict[str, int]:
        data = load_seed_data()
        counts = {"labs": 0, "benchmarks": 0, "models": 0, "sources": 0, "scores": 0}

        from app.registry import load_benchmarks, load_labs

        for row in load_labs():
            session.merge(models.Lab(**row))
            counts["labs"] += 1

        for row in load_benchmarks():
            session.merge(models.Benchmark(**row))
            counts["benchmarks"] += 1

        for row in data.get("models", []):
            session.merge(models.Model(**self._coerce_dates(row)))
            counts["models"] += 1

        for row in data.get("sources", []):
            session.merge(models.Source(**self._coerce_dates(row)))
            counts["sources"] += 1

        session.flush()
        for payload in data.get("scores", []):
            errors = validate_score_payload(payload, session)
            if errors:
                raise ValueError(f"Invalid seed score for {payload.get('model_id')}: {errors}")
            if not score_exists(session, payload):
                session.add(models.ReportedBenchmarkScore(**self._coerce_dates(payload)))
                counts["scores"] += 1

        session.commit()
        return counts
