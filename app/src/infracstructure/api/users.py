from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.src.core.models.user import UserInputModel, UserResponseModel, UserUpdateModel
from app.src.core.security.token import create_token, decode_token
from app.src.infracstructure.auth.auth import authenticate_user, get_current_user

from .dependencies import UserServiceDP

router = APIRouter(prefix="/users", tags=["Users 👥"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserInputModel, user_service: UserServiceDP):
    existing_user = (await user_service.get_user_by_username(user.username)) or (
        await user_service.get_user_by_email(user.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this username and email already exists",
        )

    await user_service.add_user(user)

    return {"message": "User registered successfully", "user": user}


@router.post("/login")
async def token(
    user_service: UserServiceDP,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await authenticate_user(user_service, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_token(data={"sub": str(user.id)}, token_type="access")

    refresh_token = create_token(data={"sub": str(user.id)}, token_type="refresh")

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
async def refresh(refresh_token: str):
    payload = decode_token(refresh_token)

    if payload["type"] != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    access_token = create_token(
        data={"sub": payload["sub"]},
        token_type="access",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
async def get_me(current_user: UserResponseModel = Depends(get_current_user)):
    return current_user


@router.delete("/me")
async def delete_me(
    user_service: UserServiceDP,
    current_user: UserResponseModel = Depends(get_current_user),
):
    await user_service.delete_user(current_user.id)
    return {"message": "User deleted successfully"}


@router.patch("/me")
async def update_me(
    user: UserUpdateModel,
    user_service: UserServiceDP,
    current_user: UserResponseModel = Depends(get_current_user),
):
    await user_service.update_user(current_user.id, user)
    return {"message": "User updated successfully"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}
