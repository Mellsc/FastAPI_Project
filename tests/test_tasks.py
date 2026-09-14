from http import HTTPStatus

import pytest

from fast_zero.models import Todo, TodoState
from tests.conftest import TodoFactory


@pytest.mark.asyncio
async def test_create_task(client, token, mock_db_time):
    with mock_db_time(model=Todo) as time:
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
            "created_at": time.isoformat(),
            "updated_at": time.isoformat(),
        }


@pytest.mark.asyncio
async def test_filter_by_title(session, user, client, token):
    expected_user = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, title="Test todo 1")
    )
    await session.commit()

    response = client.get(
        "/tasks/?title=Test todo 1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_user


@pytest.mark.asyncio
async def test_filter_by_description(session, user, client, token):
    expected_user = 5

    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, description="description")
    )
    await session.commit()

    response = client.get(
        "/tasks/?description=desc",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_user


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
async def test_all_tasks_params(session, user, client, token):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title="Test todo combined",
            description="combined description",
            state=TodoState.done,
        )
    )

    session.add_all(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title="Other title",
            description="other description",
            state=TodoState.todo,
        )
    )
    await session.commit()

    response = client.get(
        "/tasks/?title=Test todo combined&description=combined&state=done",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


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


@pytest.mark.asyncio
async def test_delete_task(session, user, client, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()

    response = client.delete(
        f"/tasks/{todo.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.json() == {
        "message": "Task has been deleted successfully."
    }


def test_delete_wrong_user(client, token):
    response = client.delete(
        f"/tasks/{10}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found."}


def test_patch_todo_error(client, token):
    response = client.patch(
        "/todos/10",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Not Found"}


@pytest.mark.asyncio
async def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()

    response = client.patch(
        f"/todos/{todo.id}",
        json={"title": "teste!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "teste!"
