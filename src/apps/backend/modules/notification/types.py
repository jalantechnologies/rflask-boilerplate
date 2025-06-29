from dataclasses import dataclass
from typing import Any, Dict, Optional

from modules.account.types import PhoneNumber


@dataclass(frozen=True)
class EmailSender:
    email: str
    name: str


@dataclass(frozen=True)
class EmailRecipient:
    email: str


@dataclass(frozen=True)
class SendEmailParams:
    recipient: EmailRecipient
    sender: EmailSender
    template_id: str
    template_data: Dict[str, Any] | None = None


@dataclass(frozen=True)
class SendSMSParams:
    message_body: str
    recipient_phone: PhoneNumber


@dataclass(frozen=True)
class PushNotificationParams:
    title: str
    message: str
    device_type: Optional[str] = None
    topic: str = "all_users"
    data: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None


@dataclass(frozen=True)
class CommunicationErrorCode:
    VALIDATION_ERROR = "COMMUNICATION_ERR_01"
    SERVICE_ERROR = "COMMUNICATION_ERR_02"
    PUSH_NOTIFICATION_ERROR = "COMMUNICATION_ERR_03"


@dataclass(frozen=True)
class ValidationFailure:
    field: str
    message: str
