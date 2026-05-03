from __future__ import annotations

from connectors.base import SourceConnector


def fetch_raw_snapshots(connectors: list[SourceConnector]) -> list[dict]:
    raw_items: list[dict] = []
    for connector in connectors:
        raw_items.extend(connector.fetch_raw())
    return raw_items

