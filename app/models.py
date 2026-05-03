from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Lab(Base):
    __tablename__ = "labs"

    lab_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    website: Mapped[str | None] = mapped_column(String)
    source_urls: Mapped[list[str]] = mapped_column(JSON, default=list)
    notes: Mapped[str | None] = mapped_column(Text)


class Model(Base):
    __tablename__ = "models"

    model_id: Mapped[str] = mapped_column(String, primary_key=True)
    lab_id: Mapped[str] = mapped_column(ForeignKey("labs.lab_id"), index=True)
    canonical_name: Mapped[str] = mapped_column(String, nullable=False)
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list)
    release_date: Mapped[date | None] = mapped_column(Date)
    model_family: Mapped[str | None] = mapped_column(String)
    openness: Mapped[str] = mapped_column(String, default="unknown", index=True)
    license: Mapped[str | None] = mapped_column(String)
    parameter_count_total: Mapped[float | None] = mapped_column(Float)
    parameter_count_active: Mapped[float | None] = mapped_column(Float)
    context_window_tokens: Mapped[int | None] = mapped_column(Integer)
    modalities: Mapped[list[str]] = mapped_column(JSON, default=list)
    supports_tools: Mapped[bool | None] = mapped_column(Boolean)
    supports_json_schema: Mapped[bool | None] = mapped_column(Boolean)
    input_price_usd_per_mtok: Mapped[float | None] = mapped_column(Float)
    output_price_usd_per_mtok: Mapped[float | None] = mapped_column(Float)
    model_card_url: Mapped[str | None] = mapped_column(String)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Benchmark(Base):
    __tablename__ = "benchmarks"

    benchmark_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    family: Mapped[str] = mapped_column(String, index=True)
    capability: Mapped[str] = mapped_column(String, index=True)
    modality: Mapped[str] = mapped_column(String, default="text")
    primary_metric: Mapped[str] = mapped_column(String)
    higher_is_better: Mapped[bool] = mapped_column(Boolean, default=True)
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list)
    description: Mapped[str | None] = mapped_column(Text)
    official_url: Mapped[str | None] = mapped_column(String)
    contamination_risk: Mapped[str] = mapped_column(String, default="unknown")
    benchmark_status: Mapped[str] = mapped_column(String, default="unknown")
    notes: Mapped[str | None] = mapped_column(Text)


class Source(Base):
    __tablename__ = "sources"

    source_id: Mapped[str] = mapped_column(String, primary_key=True)
    source_name: Mapped[str] = mapped_column(String, nullable=False)
    source_type: Mapped[str] = mapped_column(String, index=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str | None] = mapped_column(String)
    published_at: Mapped[date | None] = mapped_column(Date)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    content_hash: Mapped[str | None] = mapped_column(String)
    license: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)


class ReportedBenchmarkScore(Base):
    __tablename__ = "reported_benchmark_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lab_id: Mapped[str] = mapped_column(ForeignKey("labs.lab_id"), index=True)
    model_id: Mapped[str] = mapped_column(ForeignKey("models.model_id"), index=True)
    model_display_name: Mapped[str] = mapped_column(String, nullable=False)
    model_release_date: Mapped[date | None] = mapped_column(Date)
    benchmark_id: Mapped[str] = mapped_column(ForeignKey("benchmarks.benchmark_id"), index=True)
    benchmark_family: Mapped[str] = mapped_column(String, index=True)
    benchmark_variant: Mapped[str | None] = mapped_column(String)
    capability: Mapped[str] = mapped_column(String, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    score_unit: Mapped[str] = mapped_column(String, nullable=False)
    higher_is_better: Mapped[bool] = mapped_column(Boolean, nullable=False)
    eval_setting: Mapped[str | None] = mapped_column(String)
    num_trials: Mapped[int | None] = mapped_column(Integer)
    pass_at_k: Mapped[int | None] = mapped_column(Integer)
    context_setting: Mapped[str | None] = mapped_column(String)
    scaffold: Mapped[str | None] = mapped_column(String)
    source_type: Mapped[str] = mapped_column(String, index=True)
    source_url: Mapped[str] = mapped_column(String, nullable=False)
    source_title: Mapped[str | None] = mapped_column(String)
    source_published_at: Mapped[date | None] = mapped_column(Date)
    extracted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    snapshot_week: Mapped[date] = mapped_column(Date, index=True)
    extraction_method: Mapped[str] = mapped_column(String, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    verification_status: Mapped[str] = mapped_column(String, nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    raw_quote: Mapped[str | None] = mapped_column(Text)
    raw_table_json: Mapped[dict | None] = mapped_column(JSON)
    normalized_json: Mapped[dict | None] = mapped_column(JSON)


class PendingExtraction(Base):
    __tablename__ = "pending_extractions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_id: Mapped[str] = mapped_column(String, index=True)
    candidate_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reviewer_notes: Mapped[str | None] = mapped_column(Text)

