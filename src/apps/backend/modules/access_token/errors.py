from modules.access_token.types import AccessTokenErrorCode
from modules.error.custom_errors import AppError


class AccessTokenInvalidError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=AccessTokenErrorCode.ACCESS_TOKEN_INVALID, http_status_code=401, message=message)


class AccessTokenExpiredError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=AccessTokenErrorCode.ACCESS_TOKEN_EXPIRED, http_status_code=401, message=message)


class UnauthorizedAccessError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=AccessTokenErrorCode.UNAUTHORIZED_ACCESS, http_status_code=401, message=message)


class AuthorizationHeaderNotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(
            code=AccessTokenErrorCode.AUTHORIZATION_HEADER_NOT_FOUND, http_status_code=401, message=message
        )


class InvalidAuthorizationHeaderError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=AccessTokenErrorCode.INVALID_AUTHORIZATION_HEADER, http_status_code=401, message=message)
