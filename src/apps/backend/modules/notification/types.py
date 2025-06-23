# src/apps/backend/modules/notification/types.py
from dataclasses import dataclass
from typing import Any, Dict, List

from modules.account.types import PhoneNumber


@dataclass(frozen=True)
class EmailSender:
    email: str
    name: str


@dataclass(frozen=True)
class EmailRecipient:
    email: str
    name: str | None = None


# Keep backward compatibility with existing code
@dataclass(frozen=True)
class SendEmailParams:
    recipients: List[EmailRecipient]  # Support multiple recipients
    sender: EmailSender
    template_id: str | None = None  # Made optional for non-template emails
    template_data: Dict[str, Any] | None = None
    subject: str | None = None  # For non-template emails
    html_content: str | None = None  # For non-template emails
    text_content: str | None = None  # For non-template emails

    # Backward compatibility property
    @property
    def recipient(self) -> EmailRecipient:
        """Backward compatibility - return first recipient"""
        return self.recipients[0] if self.recipients else None


@dataclass(frozen=True)
class BulkEmailParams:
    recipients: List[EmailRecipient]
    sender: EmailSender
    template_id: str
    personalizations: List[Dict[str, Any]] | None = None  # For personalized content per recipient


@dataclass(frozen=True)
class EmailResponse:
    success: bool
    message_id: str | None = None
    status_code: int | None = None
    errors: List[str] | None = None


@dataclass(frozen=True)
class SendSMSParams:
    message_body: str
    recipient_phone: PhoneNumber


@dataclass(frozen=True)
class CommunicationErrorCode:
    VALIDATION_ERROR = "COMMUNICATION_ERR_01"
    SERVICE_ERROR = "COMMUNICATION_ERR_02"
    MULTIPLE_RECIPIENTS_ERROR = "COMMUNICATION_ERR_03"


@dataclass(frozen=True)
class ValidationFailure:
    field: str
    message: str
