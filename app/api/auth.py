from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .auth_jwt import *
from app.db.shemas import *
from app.db import crud
from app.core import utils as auth_utils

router = APIRouter(prefix='/jwt', tags=['JWT'])

@router.post('/register', response_model=UserCreate)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already taken'
        )
    
    hashed_password = auth_utils.hash_password(user_data.password)

    new_user = crud.create_user(db, user_data.email, hashed_password)

    return UserCreate(
        email=new_user.email,
        password='hidden'
    )

@router.post('/login', response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserShema = Depends(validate_auth_user)
):
    jwt_payload = {
        'email': user.email
    }

    access_token = auth_utils.encode_jwt(jwt_payload)

    return TokenInfo(
        access_token=access_token,
        token_type='Bearer'
    )

@router.get('/users/me')
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserShemaAdmin = Depends(get_current_active_auth_user),
):
    iat = payload.get('iat')
    return {
        'email' : user.email,
        'iat' : iat,
        'is_admin': user.is_admin
    }