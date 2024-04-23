from modules.password_reset_token.types import PasswordResetTokenErrorCode
from modules.error.custom_errors import AppError


class PasswordResetTokenEmailNotEnabledForTheEnvironmentError(AppError):
    code: PasswordResetTokenErrorCode;
    
    def __init__(
        self,
    ) -> None:
        super().__init__(
            code=PasswordResetTokenErrorCode.PASSWORD_RESET_EMAIL_NOT_ENABLED_FOR_THE_ENVIRONMENT,
            http_status_code=409,
            message="Password reset token is not enabled for the environment.",
        )
        
class PasswordResetTokenNotFoundError(AppError):
    code: PasswordResetTokenErrorCode;
    
    def __init__(
        self,
    ) -> None:
        super().__init__(
            code=PasswordResetTokenErrorCode.PASSWORD_RESET_TOKEN_NOT_FOUND,
            http_status_code=404,
            message=f"System is unable to find a token with this account",
        )
