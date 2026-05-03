from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipelines.weekly_update import run_weekly_update  # noqa: E402


if __name__ == "__main__":
    print(run_weekly_update())

