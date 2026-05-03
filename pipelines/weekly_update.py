from __future__ import annotations

from connectors.manual_seed import ManualSeedConnector


def run_weekly_update() -> dict[str, object]:
    # Skeleton: the first iteration only proves the connector contract.
    connector = ManualSeedConnector()
    raw = connector.fetch_raw()
    extracted = connector.extract(raw)
    normalized = connector.normalize(extracted)
    return {
        "connector": connector.source_id,
        "raw_items": len(raw),
        "extracted_items": len(extracted),
        "normalized_items": len(normalized),
        "status": "review_required",
    }

