from dataclasses import dataclass
from typing import Any, Dict, Optional

from modules.account.types import PhoneNumber


@dataclass(frozen=True)
class SendSMSParams:
    """Parameters for sending SMS via Twilio"""

    recipient_phone: PhoneNumber
    message_body: str
    message_sid: Optional[str] = None


@dataclass(frozen=True)
class SMSNotificationErrorCode:
    """Error codes for SMS notifications"""

    VALIDATION_ERROR = "SMS_NOTIFICATION_ERR_01"
    SERVICE_ERROR = "SMS_NOTIFICATION_ERR_02"


@dataclass(frozen=True)
class SMSResponse:
    """Response from SMS service"""

    success: bool
    message_sid: Optional[str] = None
    error_message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
