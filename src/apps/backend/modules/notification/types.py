from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class NotificationRecipient:
    """Represents a notification recipient identified by FCM token"""

    fcm_token: str


@dataclass(frozen=True)
class NotificationContent:
    """
    Represents the content of a notification

    Contains the title and body text that will be displayed to the user,
    plus optional custom data for application-specific handling
    """

    title: str
    body: str
    data: Optional[Dict[str, str]] = None


@dataclass(frozen=True)
class SendNotificationParams:
    """Parameters for sending a notification to a specific recipient"""

    recipient: NotificationRecipient
    content: NotificationContent


@dataclass(frozen=True)
class NotificationErrorCode:
    """
    Standardized error codes for notification-related errors

    Using consistent error codes helps with:
    - Automated error handling in client applications
    - Easier debugging and logging
    - Clear error categorization for analytics
    """

    INVALID_TOKEN: str = "NOTIFICATION_ERR_01"
    SERVICE_ERROR: str = "NOTIFICATION_ERR_02"
    VALIDATION_ERROR: str = "NOTIFICATION_ERR_03"
    CONFIGURATION_ERROR: str = "NOTIFICATION_ERR_04"
    TOKEN_NOT_REGISTERED: str = "NOTIFICATION_ERR_05"
