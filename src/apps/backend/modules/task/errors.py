from modules.error.custom_errors import AppError
from modules.task.types import TaskErrorCode


class TaskNotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TaskErrorCode.NOT_FOUND, http_status_code=404, message=message)


class TaskWithIdNotFoundError(TaskNotFoundError):
    def __init__(self, id: str) -> None:
        super().__init__(message=f"We could not find a task with id: {id}. Please verify and try again.")


class TaskBadRequestError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TaskErrorCode.BAD_REQUEST, http_status_code=400, message=message)


class TaskAlreadyExistsError(AppError):
    def __init__(self, task_name: str) -> None:
        super().__init__(
            code=TaskErrorCode.ALREADY_EXISTS,
            http_status_code=409,
            message=f"A task with the name '{task_name}' already exists. Please choose a different name.",
        )
