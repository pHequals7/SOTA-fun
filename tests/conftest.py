from __future__ import annotations

import pytest

from app.db import SessionLocal, init_db
from connectors.manual_seed import ManualSeedConnector


@pytest.fixture(scope="session", autouse=True)
def seeded_db() -> None:
    init_db()
    with SessionLocal() as session:
        ManualSeedConnector().seed(session)

