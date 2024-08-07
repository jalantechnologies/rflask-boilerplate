from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordResetToken:
    id: str
    account: str
    expires_at: str
    is_expired: bool
    is_used: bool
    token: str


@dataclass(frozen=True)
class CreatePasswordResetTokenParams:
    username: str


@dataclass(frozen=True)
class PasswordResetTokenErrorCode:
    PASSWORD_RESET_TOKEN_NOT_FOUND: str = "PASSWORD_RESET_TOKEN_ERR_01"
