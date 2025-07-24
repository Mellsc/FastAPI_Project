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
