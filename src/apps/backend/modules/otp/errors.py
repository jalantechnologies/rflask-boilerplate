from modules.error.custom_errors import AppError
from modules.otp.types import OtpErrorCode


class OtpIncorrectError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code=OtpErrorCode.INCORRECT_OTP, http_status_code=400, message="Please provide the correct OTP to login."
        )


class OtpExpiredError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code=OtpErrorCode.OTP_EXPIRED,
            http_status_code=400,
            message="The OTP has expired. Please request a new OTP.",
        )


class OtpRequestFailedError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code=OtpErrorCode.REQUEST_FAILED, http_status_code=400, message="Please provide a valid phone number."
        )
