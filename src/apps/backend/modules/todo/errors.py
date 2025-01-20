from modules.error.custom_errors import AppError
from modules.todo.types import TodoErrorCode


class TodoNotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TodoErrorCode.NOT_FOUND, http_status_code=404, message=message)


class AccountBadRequestError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TodoErrorCode.BAD_REQUEST, http_status_code=400, message=message)
