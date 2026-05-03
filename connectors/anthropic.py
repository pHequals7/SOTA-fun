from __future__ import annotations

from connectors.base import SourceConnector


class AnthropicConnector(SourceConnector):
    source_id = "anthropic"

    def discover(self) -> list[dict]:
        # Future: watch Anthropic news, model cards, system cards, and release notes.
        raise NotImplementedError

    def fetch_raw(self) -> list[dict]:
        # Future: snapshot pages/PDFs and store content hashes under data/raw.
        raise NotImplementedError

    def extract(self, raw_items: list[dict]) -> list[dict]:
        raise NotImplementedError

    def normalize(self, extracted_items: list[dict]) -> list[dict]:
        raise NotImplementedError

    def validate(self, normalized_items: list[dict]) -> dict:
        raise NotImplementedError

