from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from zoneinfo import ZoneInfo

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.settings import settings

# funcoes que focam em seguranca da API: rash de senha e auth com token

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

SessionDep = Annotated[AsyncSession, Depends(get_session)]
Oauth2 = Annotated[OAuth2PasswordRequestForm, Depends()]

# rash de senha


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# criando token jwt


def create_access_token(
    data: dict, expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=expire_minutes
    )

    to_encode.update({"exp": expire})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# autenticação via jwt


async def get_current_user(
    session: SessionDep,
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get("sub")

        if not subject_email:
            raise credentials_exception

    except PyJWTError:
        raise credentials_exception

    user = await session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        raise credentials_exception

    return user
