from dataclasses import dataclass


@dataclass(frozen=True)
class AccountSearchParams:
  username: str
  password: str


@dataclass(frozen=True)
class CreateAccountParams:
  username: str
  password: str


@dataclass(frozen=True)
class AccountInfo:
  id: str
  username: str


@dataclass(frozen=True)
class Account:
  id: str
  username: str
  hashed_password: str
