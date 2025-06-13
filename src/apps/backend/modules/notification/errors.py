from modules.application.errors import AppError
from modules.notification.types import NotificationErrorCode


class NotificationInvalidTokenError(AppError):
    def __init__(self, token: str) -> None:
        super().__init__(
            code=NotificationErrorCode.INVALID_TOKEN,
            http_status_code=400,
            message=f"The provided FCM token '{token}' is invalid.",
        )


class NotificationServiceError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(
            code=NotificationErrorCode.SERVICE_ERROR,
            http_status_code=503,
            message=f"Notification service error: {message}",
        )


class NotificationValidationError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(
            code=NotificationErrorCode.VALIDATION_ERROR,
            http_status_code=400,
            message=f"Notification validation error: {message}",
        )


class NotificationConfigurationError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code=NotificationErrorCode.CONFIGURATION_ERROR,
            http_status_code=500,
            message="Firebase configuration is missing or invalid.",
        )


class NotificationTokenNotRegisteredError(AppError):
    def __init__(self, token: str) -> None:
        super().__init__(
            code=NotificationErrorCode.TOKEN_NOT_REGISTERED,
            http_status_code=400,
            message=f"The FCM token '{token}' is not registered or has expired.",
        )
