from http import HTTPStatus

from fastapi.testclient import TestClient
from fast_zero.schemas import UserPublic


# Testes das rotas
def test_create_user(client):

    response = client.post("/users/",
                           json = {
                              'username': 'teste',
                              'email': 'test@email.com',
                              'password': 'senhadeteste',
                              'id': 1,})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'teste',
                              'email': 'test@email.com',
                              'id': 1,}


def test_create_user_duplicate(client, user):

    response = client.post("/users/",
                            json = {
                              'username': user.username,
                              'email': 'test@email.com',
                              'password': 'senhadeteste',})
    
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}
    

def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put("/users/1",
                          json = {
                              'username': 'teste',
                              'email': 'test@email.com',
                              'password': 'senhadeteste',
                              'id': 1,
                          })
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == { 'username': 'teste',
                               'email': 'test@email.com',
                               'id': 1,}     
    

def test_delete_user(client, user):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}

