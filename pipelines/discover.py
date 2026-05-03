from __future__ import annotations

from connectors.base import SourceConnector


def discover_sources(connectors: list[SourceConnector]) -> list[dict]:
    items: list[dict] = []
    for connector in connectors:
        items.extend(connector.discover())
    return items

