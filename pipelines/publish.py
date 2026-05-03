from __future__ import annotations

from sqlalchemy.orm import Session

from app import models
from app.validation import score_exists, validate_score_payload


def publish_scores(candidates: list[dict], session: Session) -> dict[str, int]:
    inserted = 0
    skipped = 0
    for candidate in candidates:
        errors = validate_score_payload(candidate, session)
        if errors:
            raise ValueError(f"Invalid candidate: {errors}")
        if score_exists(session, candidate):
            skipped += 1
            continue
        session.add(models.ReportedBenchmarkScore(**candidate))
        inserted += 1
    session.commit()
    return {"inserted": inserted, "skipped": skipped}

