from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SourceType(StrEnum):
    official_lab = "official_lab"
    official_benchmark = "official_benchmark"
    independent = "independent"
    provider_claim = "provider_claim"
    community = "community"
    scraped = "scraped"


class ScoreUnit(StrEnum):
    percent = "%"
    accuracy = "accuracy"
    pass_at_1 = "pass@1"
    pass_at_k = "pass@k"
    elo = "Elo"
    win_rate = "win_rate"
    resolved_rate = "resolved_rate"
    other = "other"


class ExtractionMethod(StrEnum):
    manual = "manual"
    parser = "parser"
    llm_extracted = "llm_extracted"
    api = "api"


class VerificationStatus(StrEnum):
    unverified = "unverified"
    community_verified = "community_verified"
    maintainer_verified = "maintainer_verified"
    official = "official"


class LabRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lab_id: str
    name: str
    website: str | None = None
    source_urls: list[str] = Field(default_factory=list)
    notes: str | None = None


class ModelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    model_id: str
    lab_id: str
    canonical_name: str
    aliases: list[str] = Field(default_factory=list)
    release_date: date | None = None
    model_family: str | None = None
    openness: str = "unknown"
    license: str | None = None
    parameter_count_total: float | None = None
    parameter_count_active: float | None = None
    context_window_tokens: int | None = None
    modalities: list[str] = Field(default_factory=list)
    supports_tools: bool | None = None
    supports_json_schema: bool | None = None
    input_price_usd_per_mtok: float | None = None
    output_price_usd_per_mtok: float | None = None
    model_card_url: str | None = None
    last_seen_at: datetime | None = None


class BenchmarkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    benchmark_id: str
    name: str
    family: str
    capability: str
    modality: str = "text"
    primary_metric: str
    higher_is_better: bool
    aliases: list[str] = Field(default_factory=list)
    description: str | None = None
    official_url: str | None = None
    contamination_risk: str = "unknown"
    benchmark_status: str = "unknown"
    notes: str | None = None


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_id: str
    source_name: str
    source_type: SourceType
    url: str
    title: str | None = None
    published_at: date | None = None
    fetched_at: datetime | None = None
    content_hash: str | None = None
    license: str | None = None
    notes: str | None = None


class ScoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lab_id: str
    model_id: str
    model_display_name: str
    model_release_date: date | None = None
    benchmark_id: str
    benchmark_family: str
    benchmark_variant: str | None = None
    capability: str
    score: float
    score_unit: ScoreUnit
    higher_is_better: bool
    eval_setting: str | None = None
    num_trials: int | None = None
    pass_at_k: int | None = None
    context_setting: str | None = None
    scaffold: str | None = None
    source_type: SourceType
    source_url: str
    source_title: str | None = None
    source_published_at: date | None = None
    extracted_at: datetime
    snapshot_week: date
    extraction_method: ExtractionMethod
    confidence: float
    verification_status: VerificationStatus
    notes: str | None = None
    raw_quote: str | None = None
    raw_table_json: dict[str, Any] | None = None
    normalized_json: dict[str, Any] | None = None


class BenchmarkResolveRequest(BaseModel):
    query: str


class BenchmarkResolveMatch(BaseModel):
    benchmark_id: str
    name: str
    confidence: float
    reason: str


class BenchmarkResolveResponse(BaseModel):
    matches: list[BenchmarkResolveMatch]


class RankingResult(BaseModel):
    rank: int
    model_id: str
    model: str
    lab: str
    score: float
    unit: str
    eval_setting: str | None = None
    source_type: str
    source_url: str
    source_published_at: date | None = None
    comparability_warning: str | None = None


class RankingResponse(BaseModel):
    benchmark: dict[str, Any]
    snapshot_week: date | None = None
    ranking_mode: str
    results: list[RankingResult]
    warnings: list[str] = Field(default_factory=list)


class UseCaseRead(BaseModel):
    use_case_id: str
    description: str
    benchmarks: list[str]


class SnapshotRead(BaseModel):
    snapshot_week: date | None = None
    files: dict[str, str]
    row_counts: dict[str, int]

