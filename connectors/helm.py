from __future__ import annotations

from connectors.anthropic import AnthropicConnector


class HELMConnector(AnthropicConnector):
    source_id = "helm"
    # Future: ingest HELM run metadata, benchmark variants, and scenario-level scores.

