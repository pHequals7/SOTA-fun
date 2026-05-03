from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_session
from app.rankings import top_for_benchmark
from app.schemas import RankingResponse

router = APIRouter(prefix="/v1/benchmarks", tags=["rankings"])


@router.get("/{benchmark_id}/top", response_model=RankingResponse)
def benchmark_top(
    benchmark_id: str,
    k: int = 3,
    mode: str = "reported_latest",
    openness: str | None = None,
    lab: str | None = None,
    source_type: str | None = None,
    snapshot_week: date | None = None,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    if mode not in {"reported_latest", "comparable_only", "best_available"}:
        raise HTTPException(status_code=422, detail="invalid ranking mode")
    try:
        return top_for_benchmark(
            session,
            benchmark_id=benchmark_id,
            k=k,
            mode=mode,
            openness=openness,
            lab=lab,
            source_type=source_type,
            snapshot_week=snapshot_week,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="benchmark not found") from None

