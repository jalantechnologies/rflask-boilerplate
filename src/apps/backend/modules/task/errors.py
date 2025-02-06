from modules.task.types import TaskErrorCode
from modules.error.custom_errors import AppError

class TaskNotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TaskErrorCode.NOT_FOUND, http_status_code=404, message=message)

class TaskBadRequestError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TaskErrorCode.BAD_REQUEST, http_status_code=400, message=message)
