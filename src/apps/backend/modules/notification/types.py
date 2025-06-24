# src/apps/backend/modules/notification/types.py
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from modules.account.types import PhoneNumber


@dataclass(frozen=True)
class EmailSender:
    email: str
    name: str


@dataclass(frozen=True)
class EmailRecipient:
    email: str
    name: Optional[str] = None


@dataclass(frozen=True)
class SendEmailParams:
    recipients: List[EmailRecipient]
    sender: EmailSender
    template_id: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None
    subject: Optional[str] = None
    html_content: Optional[str] = None
    text_content: Optional[str] = None

    @property
    def recipient(self) -> Optional[EmailRecipient]:
        return self.recipients[0] if self.recipients else None


@dataclass(frozen=True)
class BulkEmailParams:
    recipients: List[EmailRecipient]
    sender: EmailSender
    template_id: str
    personalizations: Optional[List[Dict[str, Any]]] = None


@dataclass(frozen=True)
class EmailResponse:
    success: bool
    message_id: Optional[str] = None
    status_code: Optional[int] = None
    errors: Optional[List[str]] = None


@dataclass(frozen=True)
class SendSMSParams:
    message_body: str
    recipient_phone: PhoneNumber


class CommunicationErrorCode(Enum):
    VALIDATION_ERROR = "COMMUNICATION_ERR_01"
    SERVICE_ERROR = "COMMUNICATION_ERR_02"
    MULTIPLE_RECIPIENTS_ERR = "COMMUNICATION_ERR_03"


class SMSErrorCode(Enum):
    VALIDATION_ERROR = "SMS_ERR_01"
    SERVICE_ERROR = "SMS_ERR_02"
    BULK_SMS_ERROR = "SMS_ERR_03"
    TEMPLATE_ERROR = "SMS_ERR_04"


class FCMErrorCode(Enum):
    VALIDATION_ERROR = "FCM_ERR_01"
    SERVICE_ERROR = "FCM_ERR_02"
    INVALID_TOKEN = "FCM_ERR_03"
    TOKEN_NOT_REGISTERED = "FCM_ERR_04"
    MESSAGE_TOO_BIG = "FCM_ERR_05"
    QUOTA_EXCEEDED = "FCM_ERR_06"
    UNAVAILABLE = "FCM_ERR_07"
    INTERNAL = "FCM_ERR_08"


@dataclass(frozen=True)
class ValidationFailure:
    field: str
    message: str


@dataclass(frozen=True)
class BulkSMSParams:
    message_body: str
    recipient_phones: List[PhoneNumber]


@dataclass(frozen=True)
class PersonalizedSMSParams:
    message_template: str
    recipients_data: List[Dict[str, Any]]


@dataclass(frozen=True)
class SMSResponse:
    success: bool
    sent_count: int = 0
    failed_count: int = 0
    message_ids: Optional[List[str]] = None
    errors: Optional[List[str]] = None
    status_code: Optional[int] = None

    def __post_init__(self) -> None:
        if self.message_ids is None:
            object.__setattr__(self, "message_ids", [])
        if self.errors is None:
            object.__setattr__(self, "errors", [])


# FCM Types
@dataclass(frozen=True)
class FCMNotification:
    title: str
    body: str
    image: Optional[str] = None


@dataclass(frozen=True)
class FCMAndroidConfig:
    priority: Optional[str] = None  # "normal" or "high"
    ttl: Optional[str] = None  # Time to live
    collapse_key: Optional[str] = None
    data: Optional[Dict[str, str]] = None
    notification: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class FCMApnsConfig:
    headers: Optional[Dict[str, str]] = None
    payload: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class FCMWebpushConfig:
    headers: Optional[Dict[str, str]] = None
    data: Optional[Dict[str, str]] = None
    notification: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class SendFCMParams:
    tokens: List[str]
    notification: Optional[FCMNotification] = None
    data: Optional[Dict[str, str]] = None
    android_config: Optional[FCMAndroidConfig] = None
    apns_config: Optional[FCMApnsConfig] = None
    webpush_config: Optional[FCMWebpushConfig] = None


@dataclass(frozen=True)
class SendFCMToTopicParams:
    topic: str
    notification: Optional[FCMNotification] = None
    data: Optional[Dict[str, str]] = None
    android_config: Optional[FCMAndroidConfig] = None
    apns_config: Optional[FCMApnsConfig] = None
    webpush_config: Optional[FCMWebpushConfig] = None


@dataclass(frozen=True)
class BulkFCMParams:
    tokens: List[str]
    notification: Optional[FCMNotification] = None
    data: Optional[Dict[str, str]] = None
    android_config: Optional[FCMAndroidConfig] = None
    apns_config: Optional[FCMApnsConfig] = None
    webpush_config: Optional[FCMWebpushConfig] = None


@dataclass
class FCMResponse:
    success: bool
    sent_count: int = 0
    failed_count: int = 0
    message_ids: Optional[List[str]] = None
    errors: Optional[List[str]] = None
    failure_details: Optional[List[Dict[str, Any]]] = None

    def __post_init__(self) -> None:
        if self.message_ids is None:
            object.__setattr__(self, "message_ids", [])
        if self.errors is None:
            object.__setattr__(self, "errors", [])
        if self.failure_details is None:
            object.__setattr__(self, "failure_details", [])
