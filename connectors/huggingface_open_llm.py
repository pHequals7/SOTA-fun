from __future__ import annotations

from connectors.anthropic import AnthropicConnector


class HuggingFaceOpenLLMConnector(AnthropicConnector):
    source_id = "huggingface_open_llm"
    # Future: fetch public leaderboard exports and normalize open-weight model aliases.

