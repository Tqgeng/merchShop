from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from app.core import utils as auth_utils
from app.db import crud
from app.db.shemas import UserShema
from app.db.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

http_bearer = HTTPBearer()

def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db)
):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid email or password'
    )

    user = crud.get_user_by_email(db, email)

    if not user or not auth_utils.validate_password(
        password, user.password
    ):
        raise unauthed_exception

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User inactive'
        )
    
    return user

def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserShema:
    token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token error'
        )
    return payload

def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: Session = Depends(get_db)
) -> UserShema:
    email: str | None = payload.get('email')
    user = crud.get_user_by_email(db, email)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Token invalid (user not found)'
    )

def get_current_active_auth_user(
    user: UserShema = Depends(get_current_auth_user)
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='User inactive'
    )

def get_current_admin(
    user: UserShema = Depends(get_current_auth_user)
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized'
        )
    return user
        