# DeepSeek V4 Pro Seed Notes

Extraction date: 2026-05-03

Seeded from the official DeepSeek Hugging Face model card and the NIST/CAISI independent evaluation. CAISI rows are intentionally separate from DeepSeek-reported rows because prompt, scaffold, and token-budget settings differ.

## Seeded Rows

| Benchmark ID | Variant | Score | Source Type |
| --- | --- | ---: | --- |
| `gpqa_diamond` | `deepseek_reported_instruct_pro_max` | 90.1% | official_lab |
| `gpqa_diamond` | `caisi_developer_settings_max` | 90.0% | independent |
| `swe_bench_verified` | `deepseek_reported_instruct_pro_max` | 80.6% | official_lab |
| `swe_bench_verified` | `caisi_inspect_react_500k_weighted_tokens` | 74.0% | independent |
| `terminal_bench` | `terminal_bench_2_0_deepseek_reported_pro_max` | 67.9% | official_lab |
| `livecodebench` | `deepseek_reported_instruct_pro_max` | 93.5% | official_lab |

## Not Seeded Yet

- PortBench: no registry card.
- CTF-Archive-Diamond: no registry card.
- ARC-AGI-2 semi-private: do not map to broad `arc_agi` without a versioned card.
- OTIS-AIME-2025: do not map to `aime_2025`.

