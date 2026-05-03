from __future__ import annotations

from connectors.anthropic import AnthropicConnector


class BigCodeBenchConnector(AnthropicConnector):
    source_id = "bigcodebench"
    # Future: fetch BigCodeBench leaderboard tables and preserve benchmark version metadata.

