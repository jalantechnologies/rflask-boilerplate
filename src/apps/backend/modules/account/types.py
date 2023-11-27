from dataclasses import dataclass


@dataclass(frozen=True)
class AccountSearchParams:
  password: str
  username: str


@dataclass(frozen=True)
class CreateAccountParams:
  password: str
  username: str


@dataclass(frozen=True)
class AccountInfo:
  id: str
  username: str


@dataclass(frozen=True)
class Account:
  id: str
  hashed_password: str
  username: str


@dataclass(frozen=True)
class AccountErrorCode:
  INVALID_CREDENTIALS: str = 'ACCOUNT_ERR_03'
  NOT_FOUND: str = 'ACCOUNT_ERR_02'
  USERNAME_ALREADY_EXISTS: str = 'ACCOUNT_ERR_01'
