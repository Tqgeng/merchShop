from datetime import datetime, timedelta
import jwt
import bcrypt
from .config import settings

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    
    to_encode.update(
        exp = expire, 
        iat = now
    )

    endoded = jwt.encode(
        to_encode,
        private_key, 
        algorithm=algorithm
    )
    return endoded

def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decode = jwt.decode(
        token, 
        public_key,
        algorithms=[algorithm]
    )
    return decode

def hash_password(
    password: str
) -> str:
    
    if isinstance(password, bytes):
        password_bytes = password
    else:
        password_bytes = password.encode()

    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode()

def validate_password(
    password: str,
    hashed_password: str
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode()
    )