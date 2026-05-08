# NVIDIA Nemotron and Sarvam Seed Notes

Extraction date: 2026-05-08

This batch adds NVIDIA Nemotron 3 Super, NVIDIA Nemotron 3 Nano, Sarvam 30B, and Sarvam 105B. Rows were seeded from official Hugging Face model cards and Sarvam/NVIDIA documentation only when model, benchmark, score, protocol variant, source URL, and source date could be preserved.

## Seeded Models

| Model ID | Lab | Total Params | Active Params | Source |
| --- | --- | ---: | ---: | --- |
| `nvidia_nemotron_3_super_120b_a12b_nvfp4` | NVIDIA | 120B | 12B | NVIDIA Hugging Face model card |
| `nvidia_nemotron_3_nano_30b_a3b_nvfp4` | NVIDIA | 30B | 3.5B | NVIDIA Hugging Face model card |
| `sarvam_30b` | Sarvam AI | 30B | 2.4B | Sarvam Hugging Face model card |
| `sarvam_105b` | Sarvam AI | 105B | 10.3B | Sarvam Hugging Face model card |

## Seeded Coverage

| Model ID | Rows | Notes |
| --- | ---: | --- |
| `nvidia_nemotron_3_super_120b_a12b_nvfp4` | 14 | Uses the official NVFP4 column only; BF16/FP8 columns are intentionally not merged. |
| `nvidia_nemotron_3_nano_30b_a3b_nvfp4` | 10 | Uses the official NVFP4 column only; includes GPQA base rather than GPQA Diamond. |
| `sarvam_30b` | 12 | Uses Sarvam official model-card tables and footnoted evaluation settings. |
| `sarvam_105b` | 11 | Uses Sarvam official model-card tables and SWE-Agent harness label for SWE-bench Verified. |

## Not Seeded

- NVIDIA SciCode, HMMT, Scale AI Multi-Challenge, AA-LCR, MMLU-ProX, WMT24++, BrowseComp, and SWE-bench Multilingual were not mapped because the current registry does not have exact benchmark cards.
- Sarvam MILU, HMMT, Beyond AIME, BrowseComp, and Writing Bench were not mapped because the current registry does not have exact benchmark cards.
- Sarvam 105B API documentation states `105B+`; the Hugging Face card exposes `10.3B active`, so the dataset stores `105B` total and `10.3B` active with source notes.

