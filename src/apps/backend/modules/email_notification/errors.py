from typing import Dict, Optional

from modules.email_notification.types import EmailErrorCode


class EmailError(Exception):
    """Base class for all email notification service errors"""

    def __init__(self, message: str, code: str, details: Optional[Dict] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class EmailConfigurationError(EmailError):
    """Raised when there is an issue with the email service configuration"""

    def __init__(self, message: str, details: Optional[Dict] = None) -> None:
        super().__init__(message, EmailErrorCode.CONFIGURATION_ERROR, details)


class EmailServiceError(EmailError):
    """Raised when there is an issue with the email service provider"""

    def __init__(self, message: str, details: Optional[Dict] = None) -> None:
        super().__init__(message, EmailErrorCode.SERVICE_ERROR, details)


class EmailValidationError(EmailError):
    """Raised when there is an issue with the email data validation"""

    def __init__(self, message: str, details: Optional[Dict] = None) -> None:
        super().__init__(message, EmailErrorCode.VALIDATION_ERROR, details)


class EmailTemplateError(EmailError):
    """Raised when there is an issue with the email template"""

    def __init__(self, message: str, details: Optional[Dict] = None) -> None:
        super().__init__(message, EmailErrorCode.TEMPLATE_ERROR, details)


class EmailAPIError(EmailError):
    """Raised when there is an issue with the email service API"""

    def __init__(self, message: str, details: Optional[Dict] = None) -> None:
        super().__init__(message, EmailErrorCode.API_ERROR, details)
