from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fast_zero.settings import Settings

# Criando sessao da API
engine = create_async_engine(Settings().DATABASE_URL)


async def get_session():  # pragma: no cover
    """
    Fornece uma sessão assíncrona do banco de dados.

    Esta função é utilizada como dependência no FastAPI
    para disponibilizar uma AsyncSession aos endpoints.

    A sessão é aberta no início da requisição e fechada
    automaticamente ao final do uso.

    Yields:
        AsyncSession: sessão assíncrona conectada ao banco.
    """
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
