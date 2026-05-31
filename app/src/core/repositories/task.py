from abc import ABC, abstractmethod
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import insert, select
from sqlalchemy import update as sqlalchemy_udapte
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core.models.task import TaskInputModel, TaskResponseModel, TaskUpdateModel
from app.src.infracstructure.db.mappers.task import TaskMapper
from app.src.infracstructure.db.models.task import Tasks


class AbstractTaskRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, user_id: UUID, task_id: int
    ) -> TaskResponseModel | None: ...

    @abstractmethod
    async def get_all(self, user_id: UUID) -> list[TaskResponseModel] | None: ...

    @abstractmethod
    async def create(self, user_id: UUID, task: TaskInputModel): ...

    @abstractmethod
    async def update(self, user_id: UUID, task_id: int, task: TaskUpdateModel): ...

    @abstractmethod
    async def delete(self, user_id: UUID, task_id: int) -> None: ...


class SQLTaskRepository(AbstractTaskRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: UUID, task_id: int) -> TaskResponseModel | None:
        query = select(Tasks).filter(Tasks.user_id == user_id, Tasks.id == task_id)

        task = (await self._session.execute(query)).scalar_one_or_none()

        if task:
            return TaskMapper.to_response(task)

        return None

    async def get_all(self, user_id: UUID) -> list[TaskResponseModel] | None:

        query = select(Tasks).filter(Tasks.user_id == user_id)

        tasks = (await self._session.execute(query)).scalars().all()

        if tasks:
            return [TaskMapper.to_response(task) for task in tasks]

        return None

    async def create(self, user_id: UUID, task: TaskInputModel):
        stmt = insert(Tasks).values(user_id=user_id, **TaskMapper.to_dict(task))
        await self._session.execute(stmt)

    async def update(self, user_id: UUID, task_id: int, task: TaskUpdateModel):
        if task.is_completed:
            completed_at = datetime.utcnow()
        else:
            completed_at = None

        stmt = (
            sqlalchemy_udapte(Tasks)
            .filter(Tasks.user_id == user_id, Tasks.id == task_id)
            .values(**TaskMapper.update_to_dict(task), completed_at=completed_at)
        )
        await self._session.execute(stmt)

    async def delete(self, user_id: UUID, task_id: int) -> None:
        stmt = sqlalchemy_delete(Tasks).filter(
            Tasks.user_id == user_id, Tasks.id == task_id
        )
        await self._session.execute(stmt)
