# Qwen3.6-Plus Seed Notes

Extraction date: 2026-05-03

These rows were added from Qwen's official Qwen3.6-Plus launch blog after subagent research. Provider-reported settings are kept explicit in each variant because several rows use Qwen-specific or incompletely documented protocols.

## Seeded Rows

| Benchmark ID | Variant | Score | Source Type |
| --- | --- | ---: | --- |
| `swe_bench_verified` | `qwen_reported_internal_agent` | 78.8% | official_lab |
| `terminal_bench` | `terminal_bench_2_0` | 61.6% | official_lab |
| `mmlu_pro` | `qwen_reported_default` | 88.5% | official_lab |
| `ifeval` | `strict_prompt` | 94.3% | official_lab |
| `livecodebench` | `v6` | 87.1% | official_lab |
| `humanitys_last_exam` | `no_tools_unspecified` | 28.8% | official_lab |
| `mmmlu` | `qwen_reported_default` | 89.5% | official_lab |
| `mmmu` | `stem` | 86.0% | official_lab |
| `video_mme` | `with_subtitles` | 87.8% | official_lab |

## Source Notes

- Qwen launch blog: model metadata, 1M context claim, multimodal/tool-use framing, and benchmark tables.
- The GPQA value reported in the source was not seeded because the retrieved evidence did not safely distinguish base GPQA from GPQA Diamond.
- HLE and MMMU rows are marked `unverified` where the protocol details are too sparse for direct comparability.

## Not Seeded Yet

The following reported evaluations were not mapped into canonical score rows because they are not yet represented by precise registry cards or would require new benchmark variants:

- GPQA, due base-vs-diamond ambiguity
- SWE-bench Pro
- SWE-bench Multilingual
- QwenWebBench
- Claw-Eval
- DeepPlanning
- MCPMark
- TAU3-Bench
- WideSearch
- MMLU-Redux
- SuperGPQA
- AA-LCR
- LongBench v2
- AIME 2026
- HMMT
- OmniDocBench
- ScreenSpot Pro

