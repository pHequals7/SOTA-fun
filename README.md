# llm-benchmark-db

`llm-benchmark-db` is an open-source benchmark intelligence database and API for LLM model releases. It tracks reported benchmark scores from model labs, official benchmark leaderboards, and trusted public sources while preserving provenance, freshness, extraction method, and comparability context.

The core row-level statement is:

> Model M scored S on benchmark B under setting E, according to source X, published on date D, extracted on date T.

## What It Solves

- Find the top reported models for a specific benchmark.
- Inspect the latest known scores for a model.
- Compare open-weight models on benchmark families like GPQA, MMLU-Pro, SWE-bench Verified, and BFCL.
- See the source, protocol, scaffold, and verification state behind each score.
- Identify when two reported results are not directly comparable.

## What It Is Not

- It is not a live evaluation platform in the first version.
- It does not create a universal "best LLM" leaderboard by default.
- It does not silently merge benchmark variants.
- It does not hide source type, freshness, or evaluation settings.
- It does not infer closed-model parameter counts unless officially published.

## Architecture

```text
tracked labs + model releases
        |
official announcements / system cards / reports / leaderboards
        |
raw fetch snapshots
        |
candidate extracted benchmark rows
        |
human review / validation
        |
canonical append-only benchmark_scores dataset
        |
API + CSV/Parquet exports + docs
```

## Setup

```bash
cd /Users/pranavhari/Desktop/hacks/SOTA/llm-benchmark-db
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Seed The Database

```bash
python scripts/seed_db.py
```

The seed data is intentionally synthetic and marked as `synthetic_example` / `community` / `unverified`. It exists to prove API behavior, not to make real benchmark claims.

## Run The API

```bash
uvicorn app.main:app --reload
```

Useful endpoints:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/v1/benchmarks
curl http://127.0.0.1:8000/v1/scores
curl http://127.0.0.1:8000/v1/benchmarks/swe_bench_verified/top
curl http://127.0.0.1:8000/v1/use-cases/coding_agent/top
curl http://127.0.0.1:8000/v1/snapshots/latest
```

Benchmark resolution:

```bash
curl -X POST http://127.0.0.1:8000/v1/benchmarks/resolve \
  -H "Content-Type: application/json" \
  -d '{"query":"best benchmark for function calling"}'
```

## Export Snapshots

```bash
python scripts/export_snapshot.py
```

This writes:

- `data/snapshots/YYYY-MM-DD/benchmark_scores.csv`
- `data/snapshots/YYYY-MM-DD/benchmark_scores.parquet`
- `data/snapshots/YYYY-MM-DD/models.csv`
- `data/snapshots/YYYY-MM-DD/benchmarks.csv`
- `data/snapshots/YYYY-MM-DD/sources.csv`
- matching files under `data/snapshots/latest/`

## Data Model

Primary entities:

- `Lab`: AI labs and model publishers.
- `Model`: canonical model identity, aliases, release metadata, openness, modalities, pricing, and model-card links.
- `Benchmark`: benchmark registry card with family, capability, metric, aliases, status, and contamination risk.
- `Source`: provenance record for where a score came from.
- `ReportedBenchmarkScore`: append-only canonical score row with source, setting, extraction, verification, and snapshot fields.
- `PendingExtraction`: review queue candidate before canonical publication.
- `UseCase`: benchmark clusters for questions like coding agents, function calling, math reasoning, and long context.

## Design Rules

- Never silently merge benchmark variants.
- Never hide provenance.
- Never create a universal "best LLM" ranking by default.
- Never mix provider-reported and independent results without labeling source type.
- Never infer closed-model parameter counts unless officially published.
- Never overwrite historical scores.
- Always expose freshness and source dates.
- Always include comparability warnings where needed.
- Prefer benchmark-by-benchmark results over arbitrary composite scores.

## Contribution Guide

Community PRs can add:

- Benchmark cards in `registry/benchmarks.yaml`
- Model aliases in `registry/model_aliases.yaml`
- Lab source URLs in `registry/labs.yaml`
- Connector plugins in `connectors/`
- Verified score rows through the review workflow
- Protocol corrections
- License corrections

Score submissions must include:

- Model ID
- Benchmark ID
- Score
- Metric / score unit
- Benchmark variant or protocol
- Evaluation setting
- Source URL
- Source published date
- Extraction method
- Raw quote or table where possible
- Verification status

Benchmark card submissions should include:

```yaml
benchmark_id:
  benchmark_id: benchmark_id
  name: Human-readable name
  family: coding
  capability: software_engineering
  modality: text
  primary_metric: resolved_rate
  higher_is_better: true
  aliases: []
  description: What the benchmark measures.
  official_url: https://example.com
  contamination_risk: unknown
  benchmark_status: active
  notes: Important protocol caveats.
```

## Review Queue

The review queue is intentionally simple:

```bash
llm-benchmark-review add SOURCE_ID '{"model_id":"..."}' --confidence 0.8
llm-benchmark-review list
llm-benchmark-review accept 1 --notes "checked source table"
llm-benchmark-review reject 2 --notes "missing protocol"
llm-benchmark-review publish-accepted
```

Accepted rows are validated before insertion into the canonical append-only score table.

## Connector Roadmap

Current implementation:

- `ManualSeedConnector`: loads synthetic seed data from `registry/seed_data.yaml`.

Stubbed connectors:

- OpenAI
- Anthropic
- Google DeepMind
- Hugging Face Open LLM
- BFCL
- HELM
- LMArena
- BigCodeBench

Each real connector should preserve raw snapshots, content hashes, source dates, extraction method, and benchmark protocol metadata.

## Lab Inclusion Quiz

When adding labs, answer these questions in the PR:

1. Is this lab a model publisher, benchmark maintainer, or infrastructure/provider source?
2. What official URLs should be watched weekly?
3. Does the lab publish model cards, system cards, technical reports, or only launch posts?
4. Are its reported scores provider claims, official benchmark records, or independently verified results?
5. Are there licensing or redistribution restrictions on reported tables?
6. What aliases are commonly used for the lab and its model families?

Initial tracked labs are OpenAI, Anthropic, Google DeepMind, Meta, Mistral, DeepSeek, xAI, Qwen, Zhipu, Moonshot, Cohere, AI21, NVIDIA, Amazon, and Sarvam AI.
