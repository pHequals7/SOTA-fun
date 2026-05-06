# Parameter Metadata Notes

Updated: 2026-05-06

Parameter counts are filled only when the provider or official model card explicitly discloses them. Closed-source API models remain blank unless the lab publishes total and active parameter counts.

## Filled Parameter Counts

| Model ID | Total Parameters | Active Parameters | Source |
| --- | ---: | ---: | --- |
| `deepseek_r1` | 671B | 37B | DeepSeek Hugging Face model card |
| `deepseek_v4_pro` | 1.6T | 49B | DeepSeek Hugging Face model card |
| `kimi_k2_6` | 1T | 32B | Moonshot/Kimi Hugging Face model card |
| `glm_5_1` | 754B | 40B | Z.AI/GLM Hugging Face model card |
| `minimax_m2_5` | 229B | 10B | MiniMax Hugging Face model card |
| `mimo_v2_5_pro` | 1.02T | 42B | XiaomiMiMo Hugging Face model card |

## Intentionally Blank

Closed-source models from OpenAI, Anthropic, Google DeepMind, xAI, Meta Muse, and Qwen API releases are blank because the providers do not publish total and active parameter counts in the cited sources.

`llama_4` and `qwen3` are still generic placeholder IDs from the initial synthetic seed, so no parameter count is assigned. Those should either be removed from the active dataset or split into specific model IDs before adding parameter metadata.

