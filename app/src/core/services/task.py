from uuid import UUID

from app.src.core.models.task import TaskInputModel, TaskResponseModel, TaskUpdateModel
from app.src.core.repositories.task import AbstractTaskRepository


class TaskService:
    def __init__(self, task_repo: AbstractTaskRepository):
        self._task_repo = task_repo

    async def get_task_by_id(
        self, user_id: UUID, task_id: int
    ) -> TaskResponseModel | None:
        return await self._task_repo.get_by_id(user_id, task_id)

    async def get_all_tasks(self, user_id: UUID) -> list[TaskResponseModel] | None:
        return await self._task_repo.get_all(user_id)

    async def create_task(self, user_id: UUID, task: TaskInputModel):
        await self._task_repo.create(user_id, task)

    async def update_task(self, user_id: UUID, task_id: int, task: TaskUpdateModel):
        await self._task_repo.update(user_id, task_id, task)

    async def delete_task(self, user_id: UUID, task_id: int) -> None:
        await self._task_repo.delete(user_id, task_id)
