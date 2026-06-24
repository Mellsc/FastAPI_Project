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


def test_expire_token(client, user):
    """Verifica se um token JWT expirado é rejeitado pela API.

    O teste congela o tempo para gerar um token de acesso válido
    para um usuário autenticado. Em seguida, avança o relógio para
    além do tempo de expiração configurado para o token e realiza
    uma requisição a uma rota protegida.

    Deve retornar HTTP 401 Unauthorized e a mensagem de erro
    indicando que as credenciais não puderam ser validadas.
    """
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.email, "password": user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
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
