from __future__ import annotations

from datetime import date

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app import models
from app.comparability import combine_warnings, comparability_warnings


def latest_snapshot_week(session: Session) -> date | None:
    return session.scalar(select(func.max(models.ReportedBenchmarkScore.snapshot_week)))


def _base_score_stmt(benchmark_id: str) -> Select[tuple[models.ReportedBenchmarkScore]]:
    return select(models.ReportedBenchmarkScore).where(
        models.ReportedBenchmarkScore.benchmark_id == benchmark_id
    )


def filtered_scores(
    session: Session,
    *,
    benchmark: str | None = None,
    model: str | None = None,
    lab: str | None = None,
    capability: str | None = None,
    snapshot_week: date | None = None,
    latest_only: bool = False,
    source_type: str | None = None,
    verification_status: str | None = None,
) -> list[models.ReportedBenchmarkScore]:
    stmt = select(models.ReportedBenchmarkScore)
    if benchmark:
        stmt = stmt.where(models.ReportedBenchmarkScore.benchmark_id == benchmark)
    if model:
        stmt = stmt.where(models.ReportedBenchmarkScore.model_id == model)
    if lab:
        stmt = stmt.where(models.ReportedBenchmarkScore.lab_id == lab)
    if capability:
        stmt = stmt.where(models.ReportedBenchmarkScore.capability == capability)
    if snapshot_week:
        stmt = stmt.where(models.ReportedBenchmarkScore.snapshot_week == snapshot_week)
    if source_type:
        stmt = stmt.where(models.ReportedBenchmarkScore.source_type == source_type)
    if verification_status:
        stmt = stmt.where(models.ReportedBenchmarkScore.verification_status == verification_status)
    if latest_only:
        latest = latest_snapshot_week(session)
        if latest:
            stmt = stmt.where(models.ReportedBenchmarkScore.snapshot_week == latest)

    return list(session.scalars(stmt.order_by(models.ReportedBenchmarkScore.snapshot_week.desc())))


def latest_score_per_model(
    session: Session, benchmark_id: str, snapshot_week: date | None = None
) -> list[models.ReportedBenchmarkScore]:
    stmt = _base_score_stmt(benchmark_id)
    if snapshot_week:
        stmt = stmt.where(models.ReportedBenchmarkScore.snapshot_week == snapshot_week)

    all_scores = list(
        session.scalars(
            stmt.order_by(
                models.ReportedBenchmarkScore.model_id,
                models.ReportedBenchmarkScore.snapshot_week.desc(),
                models.ReportedBenchmarkScore.extracted_at.desc(),
            )
        )
    )
    latest_by_model: dict[str, models.ReportedBenchmarkScore] = {}
    for score in all_scores:
        latest_by_model.setdefault(score.model_id, score)
    return list(latest_by_model.values())


def comparable_scores(
    scores: list[models.ReportedBenchmarkScore],
) -> tuple[list[models.ReportedBenchmarkScore], list[str]]:
    if not scores:
        return [], []

    baseline = scores[0]
    comparable = [
        score
        for score in scores
        if score.benchmark_variant == baseline.benchmark_variant
        and score.score_unit == baseline.score_unit
        and (baseline.eval_setting is None or score.eval_setting == baseline.eval_setting)
    ]
    warnings = []
    if len(comparable) < len(scores):
        warnings.append(
            "Some latest scores were excluded because variant, unit, or evaluation setting differed."
        )
    return comparable, warnings


def top_for_benchmark(
    session: Session,
    *,
    benchmark_id: str,
    k: int = 3,
    mode: str = "reported_latest",
    openness: str | None = None,
    lab: str | None = None,
    source_type: str | None = None,
    snapshot_week: date | None = None,
) -> dict[str, object]:
    benchmark = session.get(models.Benchmark, benchmark_id)
    if not benchmark:
        raise KeyError(benchmark_id)

    latest = snapshot_week or latest_snapshot_week(session)
    scores = latest_score_per_model(session, benchmark_id, snapshot_week=latest)

    if lab:
        scores = [score for score in scores if score.lab_id == lab]
    if source_type:
        scores = [score for score in scores if score.source_type == source_type]
    if openness:
        model_ids = {
            model.model_id
            for model in session.scalars(select(models.Model).where(models.Model.openness == openness))
        }
        scores = [score for score in scores if score.model_id in model_ids]

    warnings: list[str] = []
    baseline = scores[0] if scores else None
    if mode == "comparable_only":
        scores, warnings = comparable_scores(scores)
        baseline = scores[0] if scores else baseline
    elif mode == "best_available":
        warnings.append(
            "Best available mode may mix source types, settings, scaffolds, or verification states."
        )

    scores = sorted(scores, key=lambda score: score.score, reverse=benchmark.higher_is_better)[:k]

    lab_names = {row.lab_id: row.name for row in session.scalars(select(models.Lab))}
    results = []
    for rank, score in enumerate(scores, start=1):
        score_warnings = comparability_warnings(score, baseline=baseline, latest_snapshot=latest)
        results.append(
            {
                "rank": rank,
                "model_id": score.model_id,
                "model": score.model_display_name,
                "lab": lab_names.get(score.lab_id, score.lab_id),
                "score": score.score,
                "unit": score.score_unit,
                "eval_setting": score.eval_setting,
                "source_type": score.source_type,
                "source_url": score.source_url,
                "source_published_at": score.source_published_at,
                "comparability_warning": combine_warnings(score_warnings),
            }
        )

    return {
        "benchmark": {
            "id": benchmark.benchmark_id,
            "name": benchmark.name,
            "capability": benchmark.capability,
        },
        "snapshot_week": latest,
        "ranking_mode": mode,
        "results": results,
        "warnings": warnings,
    }

