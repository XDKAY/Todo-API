from app.src.core.models.task import TaskResponseModel, TaskUpdateModel
from app.src.infracstructure.db.models.task import Tasks


class TaskMapper:
    @staticmethod
    def to_response(task: Tasks) -> TaskResponseModel:
        return TaskResponseModel.model_validate(task)

    @staticmethod
    def to_dict(task) -> dict:
        return task.model_dump()

    @staticmethod
    def update_to_dict(task: TaskUpdateModel) -> dict:
        return task.model_dump(exclude_unset=True)
