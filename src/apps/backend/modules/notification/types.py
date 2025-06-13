from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class NotificationRecipient:
    fcm_token: str


@dataclass(frozen=True)
class NotificationContent:
    title: str
    body: str
    data: Optional[Dict[str, str]] = None


@dataclass(frozen=True)
class SendNotificationParams:
    recipient: NotificationRecipient
    content: NotificationContent


@dataclass(frozen=True)
class NotificationErrorCode:
    INVALID_TOKEN: str = "NOTIFICATION_ERR_01"
    SERVICE_ERROR: str = "NOTIFICATION_ERR_02"
    VALIDATION_ERROR: str = "NOTIFICATION_ERR_03"
    CONFIGURATION_ERROR: str = "NOTIFICATION_ERR_04"
    TOKEN_NOT_REGISTERED: str = "NOTIFICATION_ERR_05"
