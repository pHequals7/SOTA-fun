from __future__ import annotations

from datetime import date

from app import models


def comparability_warnings(
    score: models.ReportedBenchmarkScore,
    baseline: models.ReportedBenchmarkScore | None = None,
    latest_snapshot: date | None = None,
) -> list[str]:
    warnings: list[str] = []

    if baseline:
        if score.benchmark_variant != baseline.benchmark_variant:
            warnings.append("Benchmark variant differs from the comparison baseline.")
        if score.eval_setting != baseline.eval_setting:
            warnings.append("Evaluation setting differs from the comparison baseline.")
        if score.scaffold != baseline.scaffold:
            warnings.append("Tool/scaffold setting differs from the comparison baseline.")
        if score.score_unit != baseline.score_unit:
            warnings.append("Score unit differs from the comparison baseline.")

    if score.source_type in {"provider_claim", "scraped"}:
        warnings.append(f"Source type is {score.source_type}; verify before direct comparison.")
    if score.verification_status == "unverified":
        warnings.append("Score is unverified.")
    if score.extraction_method == "llm_extracted" and score.confidence < 0.75:
        warnings.append("Score was LLM-extracted with low confidence.")
    if latest_snapshot and score.source_published_at:
        age_days = (latest_snapshot - score.source_published_at).days
        if age_days > 365:
            warnings.append("Source publication date is more than one year older than the snapshot.")

    return warnings


def combine_warnings(warnings: list[str]) -> str | None:
    if not warnings:
        return None
    return " ".join(dict.fromkeys(warnings))

