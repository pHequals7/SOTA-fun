from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from app.settings import settings


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


@lru_cache(maxsize=1)
def load_labs() -> list[dict[str, Any]]:
    return list(_load_yaml(settings.registry_dir / "labs.yaml").values())


@lru_cache(maxsize=1)
def load_benchmarks() -> list[dict[str, Any]]:
    return list(_load_yaml(settings.registry_dir / "benchmarks.yaml").values())


@lru_cache(maxsize=1)
def load_use_cases() -> dict[str, dict[str, Any]]:
    return _load_yaml(settings.registry_dir / "use_cases.yaml")


@lru_cache(maxsize=1)
def load_model_aliases() -> dict[str, list[str]]:
    return _load_yaml(settings.registry_dir / "model_aliases.yaml")


@lru_cache(maxsize=1)
def load_seed_data() -> dict[str, Any]:
    return _load_yaml(settings.registry_dir / "seed_data.yaml")

