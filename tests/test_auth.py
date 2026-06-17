from http import HTTPStatus

from fast_zero.models import User


def test_authenticate_user(client, user: User):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert token["access_token"]
