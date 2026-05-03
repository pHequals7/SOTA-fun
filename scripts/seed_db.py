from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal, init_db  # noqa: E402
from connectors.manual_seed import ManualSeedConnector  # noqa: E402


def main() -> None:
    init_db()
    with SessionLocal() as session:
        counts = ManualSeedConnector().seed(session)
    print(f"Seed complete: {counts}")


if __name__ == "__main__":
    main()

