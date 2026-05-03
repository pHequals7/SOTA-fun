from __future__ import annotations

from sqlalchemy.orm import Session

from app.validation import validate_score_payload


def validate_candidates(candidates: list[dict], session: Session) -> dict[str, object]:
    errors = []
    for index, candidate in enumerate(candidates):
        candidate_errors = validate_score_payload(candidate, session)
        if candidate_errors:
            errors.append({"index": index, "errors": candidate_errors})
    return {"valid": not errors, "count": len(candidates), "errors": errors}

