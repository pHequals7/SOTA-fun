from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.db import get_session
from app.resolver import resolve_benchmarks
from app.schemas import BenchmarkRead, BenchmarkResolveRequest, BenchmarkResolveResponse

router = APIRouter(prefix="/v1/benchmarks", tags=["benchmarks"])


@router.get("", response_model=list[BenchmarkRead])
def list_benchmarks(session: Session = Depends(get_session)) -> list[models.Benchmark]:
    return list(session.scalars(select(models.Benchmark).order_by(models.Benchmark.benchmark_id)))


@router.get("/{benchmark_id}", response_model=BenchmarkRead)
def get_benchmark(benchmark_id: str, session: Session = Depends(get_session)) -> models.Benchmark:
    benchmark = session.get(models.Benchmark, benchmark_id)
    if not benchmark:
        raise HTTPException(status_code=404, detail="benchmark not found")
    return benchmark


@router.post("/resolve", response_model=BenchmarkResolveResponse)
def resolve(
    request: BenchmarkResolveRequest, session: Session = Depends(get_session)
) -> dict[str, object]:
    benchmarks = list(session.scalars(select(models.Benchmark)))
    return {"matches": resolve_benchmarks(request.query, benchmarks)}

