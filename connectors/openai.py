from __future__ import annotations

from connectors.anthropic import AnthropicConnector


class OpenAIConnector(AnthropicConnector):
    source_id = "openai"
    # Future: watch OpenAI launch posts, model pages, system cards, and eval reports.

