from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union


class NotificationType(str, Enum):
    ACCOUNT = "ACCOUNT"
    MARKETING = "MARKETING"
    PROMOTIONAL = "PROMOTIONAL"
    TRANSACTIONAL = "TRANSACTIONAL"


class NotificationChannel(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"


class NotificationStatus(str, Enum):
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class NotificationPayload:
    """Base class for notification payloads. Contains common fields for all notification types."""

    subject: str
    body: str
    metadata: Optional[dict[str, Any]] = None


@dataclass(frozen=True)
class EmailPayload(NotificationPayload):
    """Email specific payload"""

    html_body: Optional[str] = None
    from_email: Optional[str] = None
    reply_to: Optional[str] = None
    attachments: Optional[list[dict[str, Any]]] = None


@dataclass(frozen=True)
class SMSPayload(NotificationPayload):
    """SMS specific payload"""

    sender_id: Optional[str] = None


@dataclass(frozen=True)
class PushPayload(NotificationPayload):
    """Push notification specific payload"""

    title: str
    icon: Optional[str] = None
    image: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    action_buttons: Optional[list[dict[str, str]]] = None


NotificationPayloadType = Union[EmailPayload, SMSPayload, PushPayload, NotificationPayload]


@dataclass(frozen=True)
class CreateNotificationParams:
    user_id: str
    type: NotificationType
    channels: list[NotificationChannel]
    payload: NotificationPayloadType
    schedule_at: Optional[datetime] = None
    bulk_ids: Optional[list[str]] = None  # For bulk notifications


@dataclass(frozen=True)
class NotificationSearchParams:
    id: str


@dataclass(frozen=True)
class NotificationSearchByUserIdParams:
    user_id: str
    limit: int = 20
    offset: int = 0


@dataclass(frozen=True)
class Notification:
    id: str
    user_id: str
    type: NotificationType
    channels: list[NotificationChannel]
    payload: NotificationPayloadType
    status: NotificationStatus
    created_at: datetime
    updated_at: datetime
    schedule_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    workflow_id: Optional[str] = None  # Temporal workflow ID if applicable


@dataclass(frozen=True)
class NotificationLog:
    id: str
    notification_id: str
    user_id: str
    channel: NotificationChannel
    status: NotificationStatus
    attempt: int
    error_message: Optional[str] = None
    provider_response: Optional[dict[str, Any]] = None
    created_at: datetime


@dataclass(frozen=True)
class NotificationPreference:
    id: str
    user_id: str
    type: NotificationType
    email_opt_in: bool = True
    sms_opt_in: bool = True
    push_opt_in: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class UpdateNotificationPreferenceParams:
    user_id: str
    type: NotificationType
    email_opt_in: Optional[bool] = None
    sms_opt_in: Optional[bool] = None
    push_opt_in: Optional[bool] = None


@dataclass(frozen=True)
class NotificationErrorCode:
    NOT_FOUND: str = "NOTIFICATION_ERR_01"
    INVALID_PARAMS: str = "NOTIFICATION_ERR_02"
    CHANNEL_DISABLED: str = "NOTIFICATION_ERR_03"
    PROVIDER_ERROR: str = "NOTIFICATION_ERR_04"
    SCHEDULING_ERROR: str = "NOTIFICATION_ERR_05"
    USER_NOT_FOUND: str = "NOTIFICATION_ERR_06"
    BAD_REQUEST: str = "NOTIFICATION_ERR_07"
