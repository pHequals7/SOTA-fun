from __future__ import annotations

from connectors.base import SourceConnector


def extract_candidates(connector: SourceConnector, raw_items: list[dict]) -> list[dict]:
    return connector.extract(raw_items)

