# MiniMax-M2.5 Seed Notes

Extraction date: 2026-05-03

These rows were added from MiniMax's official launch post, Hugging Face model card/eval metadata, and the SWE-bench leaderboard after subagent research. MiniMax was also added to the tracked lab registry for this batch.

## Seeded Rows

| Benchmark ID | Variant | Score | Source Type |
| --- | --- | ---: | --- |
| `swe_bench_verified` | `verified_minimax_reported_claude_code_scaffold_avg_4_runs` | 80.2% | official_lab |
| `swe_bench_verified` | `verified_droid_default_prompt` | 79.7% | official_lab |
| `swe_bench_verified` | `verified_opencode_default_prompt` | 76.1% | official_lab |
| `swe_bench_verified` | `verified_mini_swe_agent_v2_high_reasoning_attempts_1` | 75.8% | official_benchmark |
| `gpqa_diamond` | `diamond_huggingface_eval_result` | 85.2% | official_lab |
| `humanitys_last_exam` | `no_tools_huggingface_eval_result` | 19.4% | official_lab |
| `aime_2025` | `official_appendix_internal_test_artificial_analysis_methods` | 86.3% | official_lab |

## Source Notes

- MiniMax launch post: release metadata, open-weight status, pricing, and SWE-bench Verified scaffold results.
- SWE-bench leaderboard: independent benchmark-maintainer row for mini-SWE-agent plus MiniMax-M2.5.
- Hugging Face model card/eval metadata: parameter counts, context length, license, GPQA Diamond, HLE, and AIME 2025 evidence.
- Multiple SWE-bench Verified rows are kept as separate variants because scaffold choice changes comparability.

## Not Seeded Yet

The following reported evaluations were not mapped into canonical score rows because the current registry does not yet have exact benchmark cards or the evidence did not expose enough protocol detail:

- Multi-SWE-Bench
- BrowseComp
- SWE-bench Multilingual
- SWE-bench Pro
- IFBench placeholder
- SciCode
- AA-LCR
- GDPval-MM
- GDPval-AA
- AA-Omniscience

