from fastapi import APIRouter, Depends

from app.src.core.models.task import TaskInputModel, TaskUpdateModel
from app.src.core.models.user import UserResponseModel
from app.src.infracstructure.api.dependencies import PaginationDP, TaskServiceDP
from app.src.infracstructure.auth.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_tasks(
    pagination: PaginationDP,
    task_service: TaskServiceDP,
    current_user: UserResponseModel = Depends(get_current_user),
):
    list_tasks = await task_service.get_all_tasks(current_user.id, pagination)

    return list_tasks


@router.get("/{task_id}")
async def get_task(
    task_id: int,
    task_service: TaskServiceDP,
    current_user: UserResponseModel = Depends(get_current_user),
):
    task = await task_service.get_task_by_id(current_user.id, task_id)

    return {
        "task": task,
    }


@router.post("/")
async def create_task(
    task: TaskInputModel,
    task_service: TaskServiceDP,
    current_user: UserResponseModel = Depends(get_current_user),
):
    await task_service.create_task(current_user.id, task)

    return {
        "task": task,
        "message": "Task created successfully",
    }


@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    task: TaskUpdateModel,
    task_service: TaskServiceDP,
    current_user: UserResponseModel = Depends(get_current_user),
):
    await task_service.update_task(current_user.id, task_id, task)


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    task_service: TaskServiceDP,
    current_user: UserResponseModel = Depends(get_current_user),
):
    await task_service.delete_task(current_user.id, task_id)

    return {
        "message": f"Task: {task_id} deleted successfully",
    }
