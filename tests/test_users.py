from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.models import User


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "teste",
            "email": "test@email.com",
            "password": "senhadeteste",
            "id": 1,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "teste",
        "email": "test@email.com",
        "id": 1,
    }


def test_create_user_duplicate(client: TestClient, user: User):
    response = client.post(
        "/users/",
        json={
            "username": "teste",
            "email": "test@email.com",
            "password": "senhadeteste",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_read_users(client):
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "teste",
            "email": "test@email.com",
            "password": "senhadeteste",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "teste",
        "email": "test@email.com",
        "id": user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK