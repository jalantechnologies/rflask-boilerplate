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
