from modules.comment.types import CommentErrorCode
from modules.error.custom_errors import AppError


class CommentNotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=CommentErrorCode.NOT_FOUND, http_status_code=404, message=message)


class CommentCreationError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=CommentErrorCode.CREATION_ERROR, http_status_code=500, message=message)


class CommentBadRequestError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=CommentErrorCode.BAD_REQUEST, http_status_code=400, message=message)


class CommentServiceError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=CommentErrorCode.SERVICE_ERROR, http_status_code=500, message=message)


class DatabaseError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=CommentErrorCode.DATABASE_ERROR, http_status_code=500, message=message)


class CommentUpdateError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=CommentErrorCode.UPDATE_ERROR, http_status_code=400, message=message)
