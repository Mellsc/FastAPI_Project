from http import HTTPStatus

from fastapi.testclient import TestClient



def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "username": "testusername",
            "password": "password",
            "email": "exemplo@gmail.com",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "testusername",
        "id": 1,
        "email": "exemplo@gmail.com",
    }


def test_read_users(client: TestClient):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "testusername",
                "id": 1,
                "email": "exemplo@gmail.com",
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "testusername2",
            "password": "password",
            "id": 1,
            "email": "exemplo2@gmail.com",
        },
    )

    assert response.json() == {
        "username": "testusername2",
        "email": "exemplo2@gmail.com",
        "id": 1,
    }


def update_invalid_user(client):
    response = client.put("/users/500")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}



def test_update_user_id(client):
    response = client.put(
        "/users/909",
        json={
            "id": 909,
            "username": "testusername2",
            "password": "password",
            "email": "exemplo2@gmail.com",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.json() == {"message": "User deleted!"}


def test_delete_invalid_user(client):
    response = client.delete("/users/909")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}