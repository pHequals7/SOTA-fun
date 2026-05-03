from __future__ import annotations

from connectors.base import SourceConnector


def normalize_candidates(connector: SourceConnector, extracted_items: list[dict]) -> list[dict]:
    return connector.normalize(extracted_items)

