import pytest

from fast_zero.models import TodoState
from tests.conftest import TodoFactory


def test_create_task(client, token):
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test todo",
            "description": "Test todo description",
            "state": "draft",
        },
    )
    assert response.json() == {
        "id": 1,
        "title": "Test todo",
        "description": "Test todo description",
        "state": "draft",
    }


@pytest.mark.asyncio
async def test_filter_by_title(session, user, client, token):
    tasks_user = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, title="Test todo 1")
    )
    await session.commit()

    response = client.get(
        "/tasks/?title=Test todo 1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == tasks_user

