from modules.error.custom_errors import AppError
from modules.otp.types import OTPErrorCode


class OTPIncorrectError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code=OTPErrorCode.INCORRECT_OTP, http_status_code=400, message="Please provide the correct OTP to login."
        )


class OTPExpiredError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code=OTPErrorCode.OTP_EXPIRED,
            http_status_code=400,
            message="The OTP has expired. Please request a new OTP.",
        )


class OTPRequestFailedError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code=OTPErrorCode.REQUEST_FAILED, http_status_code=400, message="Please provide a valid phone number."
        )
