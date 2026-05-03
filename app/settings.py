from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "local")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./llm_benchmark.db")
    registry_dir: Path = ROOT_DIR / "registry"
    snapshot_dir: Path = ROOT_DIR / "data" / "snapshots"


settings = Settings()

