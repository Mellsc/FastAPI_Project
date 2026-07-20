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


@pytest.mark.asyncio
async def test_filter_by_descripition(session, user, client, token):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, description="description")
    )
    await session.commit()

    response = client.get(
        "/tasks/?description=desc",
        headers={"Authorization": f"Bearer {token}"}),

    assert len(response.json()["todos"]) == expected_todos


@pytest.mark.asyncio
async def test_filter_by_state(session, user, client, token):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )
    await session.commit()

    response = client.get(
        "/tasks/?state=draft",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos



@pytest.mark.asyncio
async def test_all_tasks_params(
    session, user, client, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test todo combined',
            description='combined description',
            state=TodoState.done,
        )
    )

    session.add_all(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TodoState.todo,
        )
    )
    await session.commit()

    response = client.get(
        '/todos/?title=Test todo combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_todos_pagination(session, user, client, token):
    pagination_todo = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        "/tasks/?offset=1&limit=2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == pagination_todo
