import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import table_registry


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture()
def client(db_session):
    def session_test_mock():
        return db_session

    app.dependency_overrides[get_session] = session_test_mock

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()



