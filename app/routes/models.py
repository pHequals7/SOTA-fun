from __future__ import annotations

from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.db import get_session
from app.schemas import ModelRead, ScoreRead

router = APIRouter(prefix="/v1/models", tags=["models"])


@router.get("", response_model=list[ModelRead])
def list_models(session: Session = Depends(get_session)) -> list[models.Model]:
    return list(session.scalars(select(models.Model).order_by(models.Model.model_id)))


@router.get("/{model_id}", response_model=ModelRead)
def get_model(model_id: str, session: Session = Depends(get_session)) -> models.Model:
    model = session.get(models.Model, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="model not found")
    return model


@router.get("/{model_id}/benchmark-scores")
def get_model_scores(model_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    model = session.get(models.Model, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="model not found")

    stmt = (
        select(models.ReportedBenchmarkScore)
        .where(models.ReportedBenchmarkScore.model_id == model_id)
        .order_by(
            models.ReportedBenchmarkScore.benchmark_id,
            models.ReportedBenchmarkScore.snapshot_week.desc(),
        )
    )
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for score in session.scalars(stmt):
        grouped[score.benchmark_id].append(ScoreRead.model_validate(score).model_dump(mode="json"))
    return {"model": ModelRead.model_validate(model).model_dump(mode="json"), "scores": grouped}

