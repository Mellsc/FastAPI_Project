from contextlib import contextmanager
from datetime import datetime

import factory
import factory.fuzzy
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import Todo, TodoState, User, table_registry
from fast_zero.security import get_password_hash


@pytest_asyncio.fixture(scope="session")
async def engine():
    with PostgresContainer("postgres:17", driver="psycopg") as postgres:
        _engine = create_async_engine(postgres.get_connection_url())
        yield _engine


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def client(session):
    """
    Cria um cliente de testes para a aplicação FastAPI.

    Substitui a dependência get_session pela sessão
    de testes, garantindo que as requisições utilizem
    o banco temporário durante os testes.
    """

    def session_test_mock():
        return session

    app.dependency_overrides[get_session] = session_test_mock

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    """
    Mocka automaticamente campos de data do model.

    Define valores fixos para created_at e updated_at
    antes da inserção no banco, facilitando testes
    envolvendo datas e horários.
    """

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time

        if hasattr(target, "updated_at"):
            target.updated_at = time

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest_asyncio.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session):
    """
    Cria um usuário temporário para testes com factory boy.

    O usuário é salvo no banco de testes e retorna
    com uma senha limpa para autenticação
    durante os testes.
    """
    pwd = "testtest"
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = pwd

    return user


@pytest_asyncio.fixture
async def second_user(session):
    """
    Cria um usuário temporário para testes com factory boy.

    O usuário é salvo no banco de testes e retorna
    com uma senha limpa para autenticação
    durante os testes.
    """
    pwd = "testtest"
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = pwd

    return user


@pytest_asyncio.fixture
def token(client, user):
    """
    Gera um token JWT de autenticação para testes.

    Realiza login com o usuário de teste e retorna
    o access_token obtido na rota de autenticação.
    """
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.clean_password},
    )

    return response.json()["access_token"]


class UserFactory(factory.Factory):
    """Essa classe e uma fabrica de dados para teste
    cria uam sequencia de usuarios randomicos"""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"test{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    password = factory.LazyAttribute(
        lambda obj: f"{obj.username}enasoiwh13943"
    )


class TodoFactory(factory.Factory):
    """Essa classe e uma fabrica de dados do modelo
    Todo gera tarefas randomicamente para testes"""

    class Meta:
        model = Todo

    title = factory.Faker("text")
    description = factory.Faker("text")
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1
