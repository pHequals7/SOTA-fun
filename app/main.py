from __future__ import annotations

from fastapi import FastAPI

from app.db import init_db
from app.routes import benchmarks, models, rankings, scores, snapshots, use_cases

app = FastAPI(
    title="LLM Benchmark DB",
    description="Canonical, versioned benchmark intelligence database for LLM model releases.",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(benchmarks.router)
app.include_router(models.router)
app.include_router(scores.router)
app.include_router(rankings.router)
app.include_router(use_cases.router)
app.include_router(snapshots.router)

