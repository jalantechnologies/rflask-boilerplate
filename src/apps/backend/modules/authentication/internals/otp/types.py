from dataclasses import dataclass
from enum import StrEnum

from modules.account.types import PhoneNumber


@dataclass(frozen=True)
class OTPStatus(StrEnum):
    EXPIRED: str = "EXPIRED"
    PENDING: str = "PENDING"
    SUCCESS: str = "SUCCESS"


@dataclass(frozen=True)
class OTP:
    id: str
    otp_code: str
    phone_number: PhoneNumber
    status: str


@dataclass(frozen=True)
class OTPErrorCode:
    INCORRECT_OTP: str = "OTP_ERR_01"
    OTP_EXPIRED: str = "OTP_ERR_02"
    REQUEST_FAILED: str = "OTP_ERR_03"


@dataclass(frozen=True)
class CreateOTPParams:
    phone_number: PhoneNumber


@dataclass(frozen=True)
class VerifyOTPParams:
    otp_code: str
    phone_number: PhoneNumber
