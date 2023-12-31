from typing import Optional
from modules.error.custom_errors import AppError
from modules.account.types import AccountErrorCode

class AccountWithUserNameExistsError(AppError):
  def __init__(
    self,
    message: str,
  ) -> None:
    super().__init__(
      code=AccountErrorCode.USERNAME_ALREADY_EXISTS,
      https_status_code=409,
      message=message,
    )

class AccountNotFoundError(AppError):
  def __init__(
    self,
    message: str,
  ) -> None:
    super().__init__(
      code=AccountErrorCode.NOT_FOUND,
      https_status_code=409,
      message=message,

    )
