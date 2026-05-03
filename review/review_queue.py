from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import typer
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app import models
from app.db import Base, SessionLocal, init_db
from pipelines.publish import publish_scores

REVIEW_DB = Path(__file__).resolve().parent / "pending_extractions.sqlite"
engine = create_engine(f"sqlite:///{REVIEW_DB}", connect_args={"check_same_thread": False})
ReviewSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
app = typer.Typer(help="Manage pending benchmark extraction review rows.")


def init_review_db() -> None:
    Base.metadata.create_all(bind=engine, tables=[models.PendingExtraction.__table__])


@app.command("add")
def add(source_id: str, candidate_json: str, confidence: float = 0.5) -> None:
    init_review_db()
    candidate: dict[str, Any] = json.loads(candidate_json)
    with ReviewSession() as session:
        session.add(
            models.PendingExtraction(
                source_id=source_id,
                candidate_json=candidate,
                confidence=confidence,
                status="pending",
            )
        )
        session.commit()
    typer.echo("Added pending extraction.")


@app.command("list")
def list_pending(status: str = "pending") -> None:
    init_review_db()
    with ReviewSession() as session:
        rows = session.scalars(
            select(models.PendingExtraction)
            .where(models.PendingExtraction.status == status)
            .order_by(models.PendingExtraction.created_at)
        )
        for row in rows:
            typer.echo(
                json.dumps(
                    {
                        "id": row.id,
                        "source_id": row.source_id,
                        "confidence": row.confidence,
                        "status": row.status,
                        "candidate_json": row.candidate_json,
                    },
                    default=str,
                )
            )


@app.command("accept")
def accept(row_id: int, notes: str | None = None) -> None:
    _update_status(row_id, "accepted", notes)


@app.command("reject")
def reject(row_id: int, notes: str | None = None) -> None:
    _update_status(row_id, "rejected", notes)


def _update_status(row_id: int, status: str, notes: str | None) -> None:
    init_review_db()
    with ReviewSession() as session:
        row = session.get(models.PendingExtraction, row_id)
        if row is None:
            raise typer.BadParameter(f"No pending extraction with id={row_id}")
        row.status = status
        row.reviewed_at = datetime.now(timezone.utc)
        row.reviewer_notes = notes
        session.commit()
    typer.echo(f"Marked {row_id} as {status}.")


@app.command("publish-accepted")
def publish_accepted() -> None:
    init_review_db()
    init_db()
    with ReviewSession() as review_session, SessionLocal() as canonical_session:
        accepted = list(
            review_session.scalars(
                select(models.PendingExtraction).where(models.PendingExtraction.status == "accepted")
            )
        )
        result = publish_scores([row.candidate_json for row in accepted], canonical_session)
    typer.echo(json.dumps(result))


if __name__ == "__main__":
    app()

