from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from freezegun import freeze_time
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import create_access_token, get_current_user, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
Oauth2 = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token", response_model=Token)
async def login_authenticate(form_data: Oauth2, session: SessionDep):
    """Autentica um usuário e gera um token JWT.

    Recebe as credenciais do usuário, valida o e-mail e a senha
    informados e, em caso de sucesso, retorna um token de acesso
    JWT para autenticação em rotas protegidas.

    Args:
        form_data: Dados de autenticação enviados pelo formulário OAuth2.
        session: Sessão assíncrona do banco de dados.

    Returns:
        Token contendo o access_token e o tipo do token.

    Raises:
        HTTPException: Retorna 401 caso as credenciais sejam inválidas.
    """
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: get_current_user):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}