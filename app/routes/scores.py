from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_session
from app.rankings import filtered_scores
from app.schemas import ScoreRead

router = APIRouter(prefix="/v1/scores", tags=["scores"])


@router.get("", response_model=list[ScoreRead])
def list_scores(
    benchmark: str | None = None,
    model: str | None = None,
    lab: str | None = None,
    capability: str | None = None,
    snapshot_week: date | None = None,
    latest_only: bool = False,
    source_type: str | None = None,
    verification_status: str | None = None,
    session: Session = Depends(get_session),
) -> list[object]:
    return filtered_scores(
        session,
        benchmark=benchmark,
        model=model,
        lab=lab,
        capability=capability,
        snapshot_week=snapshot_week,
        latest_only=latest_only,
        source_type=source_type,
        verification_status=verification_status,
    )

