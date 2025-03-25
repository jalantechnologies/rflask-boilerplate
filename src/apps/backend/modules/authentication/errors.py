from modules.authentication.types import AccessTokenErrorCode
from modules.error.custom_errors import AppError
from modules.authentication.types import PasswordResetTokenErrorCode


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

from modules.error.custom_errors import AppError
from modules.authentication.types import PasswordResetTokenErrorCode


class PasswordResetTokenNotFoundError(AppError):

    def __init__(self) -> None:
        super().__init__(
            code=PasswordResetTokenErrorCode.PASSWORD_RESET_TOKEN_NOT_FOUND,
            http_status_code=404,
            message=f"System is unable to find a token with this account",
        )
