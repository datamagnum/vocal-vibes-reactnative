from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str | Any) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_TIME)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str):
    expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRY_TIME)
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(
        to_encode, settings.REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_access_token(access_token: str):
    decoded_jwt = jwt.decode(access_token, settings.SECRET_KEY, algorithms=ALGORITHM)
    return decoded_jwt


def decode_refresh_token(access_token: str):
    decoded_jwt = jwt.decode(
        access_token, settings.REFRESH_TOKEN_SECRET_KEY, algorithms=ALGORITHM
    )
    return decoded_jwt
