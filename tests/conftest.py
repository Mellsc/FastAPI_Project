import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from fast_zero.models import table_registry
from fastapi.testclient import TestClient
from fast_zero.app import app



@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    engine = create_engine()
    table_registry.metadata.create_all(engine)

    with session(engine) as db_session:
        yield db_session

    table_registry.metadata.drop_all(engine)