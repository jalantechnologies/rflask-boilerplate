from modules.error.custom_errors import AppError
from modules.task.types import TaskErrorCode


class TaskNotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TaskErrorCode.NOT_FOUND, http_status_code=404, message=message)


class TaskCreationError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TaskErrorCode.CREATION_ERROR, http_status_code=500, message=message)


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


class TaskServiceError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TaskErrorCode.SERVICE_ERROR, http_status_code=500, message=message)


class DatabaseError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TaskErrorCode.DATABASE_ERROR, http_status_code=500, message=message)


class TaskConversionError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TaskErrorCode.CONVERSION_ERROR, http_status_code=500, message=message)
