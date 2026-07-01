from http import HTTPStatus

from freezegun import freeze_time

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


def test_invalid_auth_email(client):
    response = client.post(
        '/auth/token',
        data={'username': 'no_user@ex.com', 'password': 'notexsitpass'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_invalid_auth_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, user, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_expire_token(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.email, "password": user.clean_password})
        assert response.satus_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "wrongwrong",
                "email": "wrong@wrong.com",
                "password": "wrong",
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}
