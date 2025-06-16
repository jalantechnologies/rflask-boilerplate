from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass(frozen=True)
class EmailRecipient:
    """Represents an email recipient"""

    email: str
    name: Optional[str] = None


@dataclass(frozen=True)
class EmailSender:
    """Represents an email sender"""

    email: str
    name: Optional[str] = None


@dataclass(frozen=True)
class EmailContent:
    """
    Represents the content of an email

    Contains the subject and body of the email, which can be either
    plain text or HTML content, plus optional custom data
    """

    subject: str
    body: str
    is_html: bool = False
    template_id: Optional[str] = None
    template_data: Optional[Dict[str, str]] = None
    attachments: Optional[List[Dict[str, str]]] = None


@dataclass(frozen=True)
class SendEmailParams:
    """Parameters for sending an email to recipients"""

    to: Union[EmailRecipient, List[EmailRecipient]]
    content: EmailContent
    sender: Optional[EmailSender] = None
    cc: Optional[List[EmailRecipient]] = None
    bcc: Optional[List[EmailRecipient]] = None
    reply_to: Optional[EmailSender] = None


@dataclass(frozen=True)
class EmailLogEntry:
    """Represents a log entry for a sent email"""

    id: str
    message_id: str
    sender: EmailSender
    recipients: List[EmailRecipient]
    subject: str
    content_type: str
    status: str
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class EmailErrorCode:
    """
    Standardized error codes for email-related errors

    Using consistent error codes helps with:
    - Automated error handling in client applications
    - Easier debugging and logging
    - Clear error categorization for analytics
    """

    INVALID_RECIPIENT: str = "EMAIL_ERR_01"
    SERVICE_ERROR: str = "EMAIL_ERR_02"
    VALIDATION_ERROR: str = "EMAIL_ERR_03"
    CONFIGURATION_ERROR: str = "EMAIL_ERR_04"
    TEMPLATE_ERROR: str = "EMAIL_ERR_05"
    API_ERROR: str = "EMAIL_ERR_06"
