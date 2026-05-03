from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_session
from app.rankings import top_for_benchmark
from app.registry import load_use_cases
from app.schemas import UseCaseRead

router = APIRouter(prefix="/v1/use-cases", tags=["use-cases"])


@router.get("", response_model=list[UseCaseRead])
def list_use_cases() -> list[dict[str, object]]:
    use_cases = load_use_cases()
    return [{"use_case_id": key, **value} for key, value in use_cases.items()]


@router.get("/{use_case_id}", response_model=UseCaseRead)
def get_use_case(use_case_id: str) -> dict[str, object]:
    use_case = load_use_cases().get(use_case_id)
    if not use_case:
        raise HTTPException(status_code=404, detail="use case not found")
    return {"use_case_id": use_case_id, **use_case}


@router.get("/{use_case_id}/top")
def top_for_use_case(
    use_case_id: str,
    k: int = 3,
    mode: str = "reported_latest",
    session: Session = Depends(get_session),
) -> dict[str, object]:
    use_case = load_use_cases().get(use_case_id)
    if not use_case:
        raise HTTPException(status_code=404, detail="use case not found")

    rankings = {}
    for benchmark_id in use_case["benchmarks"]:
        try:
            rankings[benchmark_id] = top_for_benchmark(
                session, benchmark_id=benchmark_id, k=k, mode=mode
            )
        except KeyError:
            rankings[benchmark_id] = {"error": "benchmark not found"}

    return {
        "use_case_id": use_case_id,
        "description": use_case["description"],
        "ranking_mode": mode,
        "note": "No composite score is computed; leaders are returned benchmark-by-benchmark.",
        "benchmarks": rankings,
    }

