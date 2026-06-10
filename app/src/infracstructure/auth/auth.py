from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.src.core.models.user import UserResponseModel
from app.src.core.security.hashing import verify_password
from app.src.core.security.token import decode_token
from app.src.infracstructure.api.dependencies import UserServiceDP

scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


async def authenticate_user(
    user_service: UserServiceDP, username: str, password: str
) -> UserResponseModel | None:

    user = await user_service.get_user_by_username(username)

    return (
        None
        if (not user or not verify_password(password, user.hashed_password))
        else user
    )


async def get_current_user(
    user_service: UserServiceDP, access_token: Annotated[str, Depends(scheme)]
):
    payload = decode_token(access_token)

    user_id = UUID(payload.get("sub"))

    user = await user_service.get_user_by_id(user_id)

    return user
