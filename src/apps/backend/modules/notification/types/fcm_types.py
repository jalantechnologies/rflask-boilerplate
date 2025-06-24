# src/apps/backend/modules/notification/types/fcm_types.py
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class FCMErrorCode(Enum):
    INVALID_TOKEN = "invalid_token"
    TOKEN_NOT_REGISTERED = "token_not_registered"
    MESSAGE_TOO_BIG = "message_too_big"
    INVALID_REGISTRATION = "invalid_registration"
    QUOTA_EXCEEDED = "quota_exceeded"
    UNAVAILABLE = "unavailable"
    INTERNAL = "internal"
    INVALID_ARGUMENT = "invalid_argument"


@dataclass
class FCMResponse:
    success: bool
    sent_count: int = 0
    failed_count: int = 0
    message_ids: List[str] = None
    errors: List[str] = None
    failure_details: List[Dict[str, Any]] = None

    def __post_init__(self):
        if self.message_ids is None:
            self.message_ids = []
        if self.errors is None:
            self.errors = []
        if self.failure_details is None:
            self.failure_details = []


@dataclass
class FCMNotification:
    title: str
    body: str
    image: Optional[str] = None


@dataclass
class FCMAndroidConfig:
    priority: Optional[str] = None  # "normal" or "high"
    ttl: Optional[str] = None  # Time to live
    collapse_key: Optional[str] = None
    data: Optional[Dict[str, str]] = None
    notification: Optional[Dict[str, Any]] = None


@dataclass
class FCMApnsConfig:
    headers: Optional[Dict[str, str]] = None
    payload: Optional[Dict[str, Any]] = None


@dataclass
class FCMWebpushConfig:
    headers: Optional[Dict[str, str]] = None
    data: Optional[Dict[str, str]] = None
    notification: Optional[Dict[str, Any]] = None


@dataclass
class SendFCMParams:
    tokens: List[str]
    notification: Optional[FCMNotification] = None
    data: Optional[Dict[str, str]] = None
    android_config: Optional[FCMAndroidConfig] = None
    apns_config: Optional[FCMApnsConfig] = None
    webpush_config: Optional[FCMWebpushConfig] = None


@dataclass
class SendFCMToTopicParams:
    topic: str
    notification: Optional[FCMNotification] = None
    data: Optional[Dict[str, str]] = None
    android_config: Optional[FCMAndroidConfig] = None
    apns_config: Optional[FCMApnsConfig] = None
    webpush_config: Optional[FCMWebpushConfig] = None


@dataclass
class BulkFCMParams:
    tokens: List[str]
    notification: Optional[FCMNotification] = None
    data: Optional[Dict[str, str]] = None
    android_config: Optional[FCMAndroidConfig] = None
    apns_config: Optional[FCMApnsConfig] = None
    webpush_config: Optional[FCMWebpushConfig] = None
