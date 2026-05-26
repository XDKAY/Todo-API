from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core.repositories.user import SQLUserRepository
from app.src.core.services.user import UserService
from app.src.infracstructure.db.database import get_db_session

DatabaseSessionDP = Annotated[AsyncSession, Depends(get_db_session)]


async def get_user_service(session: DatabaseSessionDP) -> UserService:
    return UserService(SQLUserRepository(session))


UserServiceDP = Annotated[UserService, Depends(get_user_service)]
