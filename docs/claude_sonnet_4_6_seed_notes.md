# Claude Sonnet 4.6 Seed Notes

Extraction date: 2026-05-03

These rows were added from Anthropic's official Claude Sonnet 4.6 system card after subagent research. The seeded rows keep Anthropic's reported protocol, effort setting, scaffold, and verification caveats in the benchmark variant and notes fields.

## Seeded Rows

| Benchmark ID | Variant | Score | Source Type |
| --- | --- | ---: | --- |
| `swe_bench_verified` | `verified_adaptive_thinking_max_effort` | 79.6% | official_lab |
| `terminal_bench` | `terminal_bench_2_0` | 59.1% | official_lab |
| `osworld` | `osworld_verified` | 72.5% | official_lab |
| `gpqa_diamond` | `adaptive_thinking_max_effort` | 89.9% | official_lab |
| `aime_2025` | `no_tools_adaptive_thinking_max_effort` | 95.6% | official_lab |
| `mmmlu` | `non_english_adaptive_thinking_max_effort` | 89.3% | official_lab |
| `mcp_atlas` | `max_effort` | 61.3% | official_lab |

## Source Notes

- Anthropic system card: release metadata, model card URL, context window, pricing, modality metadata, and benchmark scores.
- AIME 2025 is marked `unverified` because the Anthropic source includes a contamination caveat.
- MCP-Atlas is marked `unverified` because the local registry card is still a placeholder-level benchmark family mapping.

## Not Seeded Yet

The following reported evaluations were not mapped into canonical score rows because the current registry does not yet have a precise benchmark card or the mapping would collapse distinct protocols:

- ARC-AGI-2 private
- SWE-bench Multilingual
- OpenRCA
- tau2-bench Retail
- tau2-bench Telecom
- GDPval-AA
- Finance Agent
- MMMU-Pro

