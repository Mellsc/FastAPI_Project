from fastapi import APIRouter, Depends, HTTPException
from fast_zero.database import get_session
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from fast_zero.schemas import Token
from fast_zero.models import User
from fast_zero.security import verify_password, create_access_token


router = APIRouter(prefix='/auth', tags=['auth'])



@router.post('/token', response_model=Token)
def login_authenticate(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code = 401, detail = 'Unauthorized')
    
    access_token = create_access_token(data={'sub': user.email})
    return{'access_token': access_token, 'token_type': 'Bearer'}
    
