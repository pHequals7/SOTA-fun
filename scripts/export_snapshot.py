from __future__ import annotations

import shutil
import sys
from datetime import date
import json
from pathlib import Path

import pandas as pd
from sqlalchemy import func, select

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import models  # noqa: E402
from app.db import SessionLocal, init_db  # noqa: E402
from app.settings import settings  # noqa: E402


TABLES = {
    "benchmark_scores": models.ReportedBenchmarkScore,
    "models": models.Model,
    "benchmarks": models.Benchmark,
    "sources": models.Source,
}


def _records_for(session, table_model, snapshot_week: date | None = None) -> list[dict]:
    stmt = select(table_model)
    if table_model is models.ReportedBenchmarkScore and snapshot_week:
        stmt = stmt.where(models.ReportedBenchmarkScore.snapshot_week == snapshot_week)
    records = []
    for row in session.scalars(stmt):
        record = {
            column.name: getattr(row, column.name)
            for column in table_model.__table__.columns
        }
        for key, value in list(record.items()):
            if isinstance(value, (dict, list)):
                record[key] = json.dumps(value, sort_keys=True)
            elif hasattr(value, "isoformat"):
                record[key] = value.isoformat()
        records.append(record)
    return records


def export_snapshot() -> Path:
    init_db()
    with SessionLocal() as session:
        snapshot_week = session.scalar(select(func.max(models.ReportedBenchmarkScore.snapshot_week)))
        if snapshot_week is None:
            snapshot_week = date.today()

        snapshot_path = settings.snapshot_dir / snapshot_week.isoformat()
        snapshot_path.mkdir(parents=True, exist_ok=True)

        for name, table_model in TABLES.items():
            records = _records_for(session, table_model, snapshot_week=snapshot_week)
            df = pd.DataFrame(records)
            df.to_csv(snapshot_path / f"{name}.csv", index=False)
            if name == "benchmark_scores":
                df.to_parquet(snapshot_path / f"{name}.parquet", index=False)

    latest_path = settings.snapshot_dir / "latest"
    if latest_path.exists():
        shutil.rmtree(latest_path)
    shutil.copytree(snapshot_path, latest_path)
    print(f"Exported snapshot to {snapshot_path} and {latest_path}")
    return snapshot_path


if __name__ == "__main__":
    export_snapshot()
