from __future__ import annotations

from connectors.anthropic import AnthropicConnector


class BFCLConnector(AnthropicConnector):
    source_id = "bfcl"
    # Future: fetch Berkeley Function Calling Leaderboard versions and protocol metadata.

