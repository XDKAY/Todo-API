from fastapi import APIRouter

from .tasks import router as tasks_router
from .users import router as users_router

routers = APIRouter(prefix="/api")

routers.include_router(users_router)
routers.include_router(tasks_router)
