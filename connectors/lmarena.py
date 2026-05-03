from __future__ import annotations

from connectors.anthropic import AnthropicConnector


class LMArenaConnector(AnthropicConnector):
    source_id = "lmarena"
    # Future: snapshot leaderboard Elo values and their publish/fetch dates.

