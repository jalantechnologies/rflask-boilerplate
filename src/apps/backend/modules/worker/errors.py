from modules.error.custom_errors import AppError
from modules.worker.types import WorkerErrorCode


class TaskIdNotFoundError(AppError):
    def __init__(self, task_id: str) -> None:
        super().__init__(
            code=WorkerErrorCode.TASK_WITH_ID_NOT_FOUND,
            http_status_code=404,
            message=f"Could not find a task with id: {task_id}. Please verify and try again.",
        )


class TaskNameNotFoundError(AppError):
    def __init__(self, task_name: str) -> None:
        super().__init__(
            code=WorkerErrorCode.TASK_WITH_NAME_NOT_FOUND,
            http_status_code=404,
            message=f"Could not find a task with name: {task_name}. Please verify and try again.",
        )
