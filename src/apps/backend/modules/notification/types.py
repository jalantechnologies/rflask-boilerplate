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
    PUSH = "PUSH"
    SMS = "SMS"


class NotificationStatus(str, Enum):
    CANCELLED = "CANCELLED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"


@dataclass(frozen=True)
class NotificationPayload:
    """Base class for notification payloads. Contains common fields for all notification types."""

    body: str
    metadata: Optional[dict[str, Any]] = None
    subject: str


@dataclass(frozen=True)
class EmailPayload(NotificationPayload):
    """Email specific payload"""

    attachments: Optional[list[dict[str, Any]]] = None
    from_email: Optional[str] = None
    html_body: Optional[str] = None
    reply_to: Optional[str] = None


@dataclass(frozen=True)
class SMSPayload(NotificationPayload):
    """SMS specific payload"""

    sender_id: Optional[str] = None


@dataclass(frozen=True)
class PushPayload(NotificationPayload):
    """Push notification specific payload"""

    action_buttons: Optional[list[dict[str, str]]] = None
    data: Optional[dict[str, Any]] = None
    icon: Optional[str] = None
    image: Optional[str] = None
    title: str


NotificationPayloadType = Union[EmailPayload, SMSPayload, PushPayload, NotificationPayload]


@dataclass(frozen=True)
class CreateNotificationParams:
    bulk_ids: Optional[list[str]] = None  # For bulk notifications
    channels: list[NotificationChannel]
    payload: NotificationPayloadType
    schedule_at: Optional[datetime] = None
    type: NotificationType
    user_id: str


@dataclass(frozen=True)
class NotificationSearchParams:
    id: str


@dataclass(frozen=True)
class NotificationSearchByUserIdParams:
    limit: int = 20
    offset: int = 0
    user_id: str


@dataclass(frozen=True)
class Notification:
    channels: list[NotificationChannel]
    created_at: datetime
    delivered_at: Optional[datetime] = None
    id: str
    payload: NotificationPayloadType
    schedule_at: Optional[datetime] = None
    status: NotificationStatus
    type: NotificationType
    updated_at: datetime
    user_id: str
    workflow_id: Optional[str] = None  # Temporal workflow ID if applicable


@dataclass(frozen=True)
class NotificationLog:
    attempt: int
    channel: NotificationChannel
    created_at: datetime
    error_message: Optional[str] = None
    id: str
    notification_id: str
    provider_response: Optional[dict[str, Any]] = None
    status: NotificationStatus
    user_id: str


@dataclass(frozen=True)
class NotificationPreference:
    created_at: datetime = field(default_factory=datetime.utcnow)
    email_opt_in: bool = True
    id: str
    push_opt_in: bool = True
    sms_opt_in: bool = True
    type: NotificationType
    updated_at: datetime = field(default_factory=datetime.utcnow)
    user_id: str


@dataclass(frozen=True)
class UpdateNotificationPreferenceParams:
    email_opt_in: Optional[bool] = None
    push_opt_in: Optional[bool] = None
    sms_opt_in: Optional[bool] = None
    type: NotificationType
    user_id: str


@dataclass(frozen=True)
class NotificationErrorCode:
    BAD_REQUEST: str = "NOTIFICATION_ERR_07"
    CHANNEL_DISABLED: str = "NOTIFICATION_ERR_03"
    INVALID_PARAMS: str = "NOTIFICATION_ERR_02"
    NOT_FOUND: str = "NOTIFICATION_ERR_01"
    PROVIDER_ERROR: str = "NOTIFICATION_ERR_04"
    SCHEDULING_ERROR: str = "NOTIFICATION_ERR_05"
    USER_NOT_FOUND: str = "NOTIFICATION_ERR_06"
