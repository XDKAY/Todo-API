from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import insert, select
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core.models.user import (
    UserInputModel,
    UserResponseModel,
    UserUpdateModel,
)
from app.src.infracstructure.db.mappers.user import UserMapper
from app.src.infracstructure.db.models.user import Users


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserResponseModel | None: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> UserResponseModel | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserResponseModel | None: ...

    @abstractmethod
    async def create(self, user: UserInputModel): ...

    @abstractmethod
    async def update(self, user_id: UUID, user: UserUpdateModel): ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> None: ...


class SQLUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> UserResponseModel | None:
        result = await self._get_user_by_filter(Users.id, user_id)
        return result

    async def get_by_username(self, username: str) -> UserResponseModel | None:
        result = await self._get_user_by_filter(Users.username, username)
        return result

    async def get_by_email(self, email: str) -> UserResponseModel | None:
        result = await self._get_user_by_filter(Users.email, email)
        return result

    async def create(self, user: UserInputModel):
        user_dto = UserMapper.to_dto(user)

        stmt = insert(Users).values(**UserMapper.to_dict(user_dto))
        await self._session.execute(stmt)

    async def update(self, user_id: UUID, user: UserUpdateModel):
        stmt = (
            sqlalchemy_update(Users)
            .filter(Users.id == user_id)
            .values(**UserMapper.update_to_dict(user))
        )
        await self._session.execute(stmt)

    async def delete(self, user_id: UUID) -> None:
        stmt = sqlalchemy_delete(Users).filter(Users.id == user_id)
        await self._session.execute(stmt)

    async def _get_user_by_filter(
        self, column: Any, value: Any
    ) -> UserResponseModel | None:
        query = select(Users).filter(column == value)

        user = (await self._session.execute(query)).scalar_one_or_none()

        if user:
            return UserMapper.to_response(user)

        return None
