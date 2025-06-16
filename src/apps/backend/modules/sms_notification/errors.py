from modules.sms_notification.types import SMSNotificationErrorCode


class SMSNotificationError(Exception):
    """Base exception class for SMS notification related errors"""

    def __init__(self, message: str, code: str = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class ValidationError(SMSNotificationError):
    """Exception raised for validation errors when sending SMS"""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, code=SMSNotificationErrorCode.VALIDATION_ERROR)


class ServiceError(SMSNotificationError):
    """Exception raised for Twilio service related errors"""

    def __init__(self, original_error=None) -> None:
        message = str(original_error) if original_error else "SMS service error"
        super().__init__(message=message, code=SMSNotificationErrorCode.SERVICE_ERROR)
        self.original_error = original_error
