# Claude Opus 4.7 Seed Notes

Extraction date: 2026-05-03

These rows were added from public sources found with Exa MCP searches. Anthropic's official launch post contains the benchmark chart as an image, while the page text exposes release metadata and methodology footnotes. Numeric score rows below are therefore marked as `provider_claim` unless independently rerun by a benchmark maintainer or third-party evaluator.

## Seeded Rows

| Benchmark ID | Variant | Score | Source Type |
| --- | --- | ---: | --- |
| `swe_bench_verified` | `verified_anthropic_reported` | 87.6% | provider_claim |
| `gpqa_diamond` | `anthropic_reported` | 94.2% | provider_claim |
| `terminal_bench` | `terminal_bench_2_0` | 69.4% | provider_claim |
| `osworld` | `osworld_verified` | 78.0% | provider_claim |
| `mcp_atlas` | `anthropic_reported_revised_grading` | 77.3% | provider_claim |
| `mmmlu` | `anthropic_reported` | 91.5% | provider_claim |
| `humanitys_last_exam` | `no_tools` | 46.9% | provider_claim |
| `humanitys_last_exam` | `with_tools` | 54.7% | provider_claim |

## Source Notes

- Anthropic official launch post: release metadata, model ID, pricing, methodology footnotes, and chart image.
- LLM Stats: public summary of Anthropic-reported launch scores for SWE-bench Verified, GPQA Diamond, and Terminal-Bench 2.0.
- getA: public summary of Anthropic-reported OSWorld-Verified and MCP-Atlas numbers.
- OfficeChai: public summary of Anthropic-reported MMMLU number.
- BinaryVerse: public summary table including Humanity's Last Exam variants.

## Not Seeded Yet

No usable public Claude Opus 4.7 score was found in the current search pass for these registry benchmarks:

- MMLU
- MMLU-Pro
- IFEval
- IFBench
- BBH
- MuSR
- GPQA
- ARC-AGI
- GSM8K
- MATH
- MATH-500
- AIME 2024
- AIME 2025
- HumanEval
- MBPP
- LiveCodeBench
- SWE-bench
- Aider Polyglot
- BigCodeBench
- BFCL
- TAU-bench
- WebArena
- MMMU
- MathVista
- ChartQA
- DocVQA
- Video-MME
- LongBench
- RULER
- Needle-in-a-Haystack
- Loogle
- LMArena
- ArenaHard
- AlpacaEval
- MT-Bench
- WildChat
- XSTest
- HarmBench
- Jailbreak / prompt-injection suites

SWE-bench Pro, BrowseComp, Finance Agent, CyberGym, CursorBench, CharXiv, and other reported Opus 4.7 evaluations were not added unless an existing benchmark registry card already represented that benchmark family and variant safely.

