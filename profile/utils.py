from datetime import datetime, UTC, timedelta

from fastapi import HTTPException
from jwt import encode, decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from starlette import status

from profile.config import pwd_context, config


def create_password_hash(password: str) -> str:
    return pwd_context.hash(secret=password)


def verify_password(hashed_password: str, plain_password: str) -> bool:
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def create_jwt(payload: dict) -> str:
    payload["exp"] = datetime.now() + timedelta(minutes=config.JWT_EXP)
    return encode(payload=payload, key=config.JWT_SECRET_KEY)


def verify_jwt(jwt: str) -> dict:
    try:
        payload = decode(jwt=jwt, key=config.JWT_SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return payload
