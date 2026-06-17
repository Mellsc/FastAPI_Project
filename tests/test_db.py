from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import User


@pytest.mark.asyncio
async def test_db_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username="teste", password="senhadeteste", email="test@email.com"
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == "teste"))

    assert asdict(user) == {
        "id": 1,
        "username": "teste",
        "password": "senhadeteste",
        "email": "test@email.com",
        "created_at": time,
        "updated_at": time,
    }
