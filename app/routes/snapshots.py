from __future__ import annotations

from datetime import date
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.schemas import SnapshotRead
from app.settings import settings

router = APIRouter(prefix="/v1/snapshots", tags=["snapshots"])


def _metadata_for(path: Path, snapshot_week: date | None) -> dict[str, object]:
    files = {
        file.name: str(file.relative_to(settings.snapshot_dir.parent.parent))
        for file in sorted(path.glob("*"))
        if file.is_file()
    }
    row_counts: dict[str, int] = {}
    for file in path.glob("*.csv"):
        with file.open("r", encoding="utf-8") as handle:
            row_counts[file.name] = max(sum(1 for _ in handle) - 1, 0)
    return {"snapshot_week": snapshot_week, "files": files, "row_counts": row_counts}


@router.get("/latest", response_model=SnapshotRead)
def latest_snapshot() -> dict[str, object]:
    path = settings.snapshot_dir / "latest"
    if not path.exists():
        return {"snapshot_week": None, "files": {}, "row_counts": {}}
    dated_dirs = []
    for child in settings.snapshot_dir.iterdir():
        if child.is_dir() and child.name != "latest":
            try:
                dated_dirs.append(date.fromisoformat(child.name))
            except ValueError:
                continue
    snapshot_week = max(dated_dirs) if dated_dirs else None
    return _metadata_for(path, snapshot_week)


@router.get("/{snapshot_week}", response_model=SnapshotRead)
def get_snapshot(snapshot_week: date) -> dict[str, object]:
    path = settings.snapshot_dir / snapshot_week.isoformat()
    if not path.exists():
        raise HTTPException(status_code=404, detail="snapshot not found")
    return _metadata_for(path, snapshot_week)
