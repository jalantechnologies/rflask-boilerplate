from dataclasses import dataclass


@dataclass(frozen=True)
class AccountSearchParams:
    password: str
    username: str


@dataclass(frozen=True)
class AccountSearchByIdParams:
    id: str


@dataclass(frozen=True)
class CreateAccountParams:
    first_name: str
    last_name: str
    password: str
    username: str


@dataclass(frozen=True)
class AccountInfo:
    id: str
    username: str


@dataclass(frozen=True)
class Account:
    id: str
    first_name: str
    last_name: str
    username: str


@dataclass(frozen=True)
class ResetPasswordParams:
    account_id: str
    new_password: str
    token: str


@dataclass(frozen=True)
class AccountErrorCode:
    INVALID_CREDENTIALS: str = "ACCOUNT_ERR_03"
    NOT_FOUND: str = "ACCOUNT_ERR_02"
    USERNAME_ALREADY_EXISTS: str = "ACCOUNT_ERR_01"
    BAD_REQUEST: str = "ACCOUNT_ERR_04"
