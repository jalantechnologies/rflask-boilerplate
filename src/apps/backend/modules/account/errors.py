from modules.account.types import AccountErrorCode, PhoneNumber
from modules.error.custom_errors import AppError


class AccountWithUserNameExistsError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=AccountErrorCode.USERNAME_ALREADY_EXISTS, http_status_code=409, message=message)


class AccountNotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=AccountErrorCode.NOT_FOUND, http_status_code=404, message=message)


class AccountWithUsernameNotFoundError(AccountNotFoundError):
    def __init__(self, username: str) -> None:
        message = f"Account with username:: {username}, not found"
        super().__init__(message=message)


class AccountWithIdNotFoundError(AccountNotFoundError):
    def __init__(self, id: str) -> None:
        message = f"Account with id:: {id}, not found"
        super().__init__(message=message)


class AccountWithPhoneNumberNotFoundError(AccountNotFoundError):
    def __init__(self, phone_number: PhoneNumber) -> None:
        message = f"Account with phone number:: {phone_number}, not found"
        super().__init__(message=message)


class AccountInvalidPasswordError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=AccountErrorCode.INVALID_CREDENTIALS, http_status_code=401, message=message)


class AccountBadRequestError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=AccountErrorCode.BAD_REQUEST, http_status_code=400, message=message)


class AccountWithPhoneNumberExistsError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=AccountErrorCode.PHONE_NUMBER_ALREADY_EXISTS, http_status_code=409, message=message)
