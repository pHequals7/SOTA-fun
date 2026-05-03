# GDM, xAI, Meta, Xiaomi, and Opus 4.6 Seed Notes

Extraction date: 2026-05-04

This batch adds seed rows for Google DeepMind Gemini 3.1 Pro Preview, xAI Grok 4.20, Meta Muse Spark, Xiaomi MiMo-V2.5-Pro, and Claude Opus 4.6. Rows were added only when a numeric score, benchmark name, model name, source URL, and source date could be preserved.

## Seeded Models

| Model ID | Lab | Primary source |
| --- | --- | --- |
| `gemini_3_1_pro_preview` | Google DeepMind | Google DeepMind model card |
| `grok_4_20` | xAI | Arena leaderboard and xAI docs |
| `muse_spark` | Meta | Meta announcement and Arena leaderboard |
| `mimo_v2_5_pro` | Xiaomi | XiaomiMiMo Hugging Face model card |
| `claude_opus_4_6` | Anthropic | Anthropic launch/system-card material and Arena leaderboard |

## Seeded Coverage

| Model ID | Rows | Notes |
| --- | ---: | --- |
| `gemini_3_1_pro_preview` | 13 | Official model-card rows plus Arena category scores. |
| `grok_4_20` | 5 | Arena category scores plus one unverified community SWE-bench row. |
| `muse_spark` | 6 | Arena category scores plus independent SWE-bench rows. |
| `mimo_v2_5_pro` | 14 | Official Xiaomi/Hugging Face evaluation rows. |
| `claude_opus_4_6` | 18 | Anthropic/Google comparison rows plus Arena category scores. |

## Benchmark Registry Change

Added `swe_bench_pro` as a distinct benchmark card. SWE-bench Pro rows are not merged with `swe_bench_verified`.

## Caution Flags

- LMArena rows are category-specific and time-varying; variants like `text_overall`, `code_arena`, `vision_arena`, and `document_arena` must not be compared as one protocol.
- Grok 4.20 SWE-bench Verified is marked `unverified` because the scaffold is not fully specified in the community source.
- Muse Spark SWE-bench rows are marked `unverified` because they come from an independent aggregation excerpt, not a Meta system card.
- Claude Opus 4.6 rows sourced from the Gemini model-card comparison table are marked `provider_claim` and `unverified`; Anthropic-sourced rows remain separate.
- MiMo-V2.5-Pro AIME 24&25 was not mapped to `aime_2024` or `aime_2025` because the source reports a combined benchmark.

