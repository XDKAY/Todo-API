from datetime import datetime, timedelta, timezone

import jwt
from fastapi import status
from fastapi.exceptions import HTTPException
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.config import settings


def create_token(data: dict, token_type: str) -> str:
    if token_type == "refresh":
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.jwt.refresh_token_expire_days
        )

    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt.access_token_expire_minutes
        )

    payload = data.copy()
    payload["exp"] = expire
    payload["type"] = token_type

    return jwt.encode(
        payload,
        settings.jwt.secret_key.get_secret_value(),
        algorithm=settings.jwt.algorithm,
    )


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt.secret_key.get_secret_value(),
            algorithms=[settings.jwt.algorithm],
            leeway=timedelta(seconds=30),
        )

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
