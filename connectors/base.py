from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SourceConnector(ABC):
    source_id: str

    @abstractmethod
    def discover(self) -> list[dict[str, Any]]:
        """Return candidate source records to fetch."""

    @abstractmethod
    def fetch_raw(self) -> list[dict[str, Any]]:
        """Fetch raw source snapshots."""

    @abstractmethod
    def extract(self, raw_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Extract candidate score rows from raw snapshots."""

    @abstractmethod
    def normalize(self, extracted_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Normalize extracted candidates into canonical score payloads."""

    @abstractmethod
    def validate(self, normalized_items: list[dict[str, Any]]) -> dict[str, Any]:
        """Validate normalized candidates before review or publishing."""

