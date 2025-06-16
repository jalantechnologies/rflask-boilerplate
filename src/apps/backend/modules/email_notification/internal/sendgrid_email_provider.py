import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from python_http_client.exceptions import HTTPError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    Bcc,
    Cc,
    Content,
    Disposition,
    DynamicTemplateData,
    Email,
    FileContent,
    FileName,
    FileType,
    Mail,
    ReplyTo,
    To,
)

from modules.config.config_service import ConfigService
from modules.email_notification.errors import (
    EmailAPIError,
    EmailConfigurationError,
    EmailServiceError,
    EmailValidationError,
)
from modules.email_notification.internal.store.email_log_model import EmailLogModel
from modules.email_notification.internal.store.email_log_repository import EmailLogRepository
from modules.email_notification.types import EmailRecipient, EmailSender, SendEmailParams
from modules.logger.logger import Logger


class SendGridEmailProvider:
    """
    SendGrid implementation of email provider

    Handles initialization of SendGrid API client and sending emails
    through the SendGrid service
    """

    _client: Optional[SendGridAPIClient] = None
    _initialized: bool = False
    _default_sender: Optional[EmailSender] = None

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize SendGrid client with API key

        The API key is loaded from environment variables or config.
        This method must be called before any emails can be sent.

        Raises:
            EmailConfigurationError: If API key is missing or invalid
        """
        try:
            api_key = None
            try:
                api_key = ConfigService[str].get_value(key="email.sendgrid.api_key")
            except Exception:
                api_key = os.environ.get("SENDGRID_API_KEY")

            if not api_key:
                raise EmailConfigurationError("SendGrid API key is not configured")

            cls._client = SendGridAPIClient(api_key)

            default_sender_email = None
            default_sender_name = None

            try:
                default_sender_email = ConfigService[str].get_value(key="email.sendgrid.default_sender.email")
                if default_sender_email:
                    try:
                        default_sender_name = ConfigService[str].get_value(key="email.sendgrid.default_sender.name")
                    except Exception:
                        pass
            except Exception:
                default_sender_email = os.environ.get("EMAIL_DEFAULT_SENDER_EMAIL")
                default_sender_name = os.environ.get("EMAIL_DEFAULT_SENDER_NAME")

            if default_sender_email:
                cls._default_sender = EmailSender(email=default_sender_email, name=default_sender_name)

            cls._initialized = True
            Logger.info(message="SendGrid email provider initialized successfully")

        except Exception as e:
            Logger.error(message=f"Failed to initialize SendGrid email provider: {str(e)}")
            raise EmailConfigurationError(f"Failed to initialize SendGrid client: {str(e)}")

    @classmethod
    def send_email(cls, params: SendEmailParams) -> Dict[str, Any]:
        """
        Send an email using SendGrid

        Args:
            params: Email parameters including recipients, content, etc.

        Returns:
            Dict with success status and message ID

        Raises:
            EmailConfigurationError: If provider is not initialized
            EmailValidationError: If email data is invalid
            EmailServiceError: If SendGrid service returns an error
        """
        if not cls._initialized or not cls._client:
            try:
                cls.initialize()
            except Exception as e:
                raise EmailConfigurationError(f"SendGrid provider not initialized: {str(e)}")

        try:

            sender = params.sender or cls._default_sender
            if not sender:
                raise EmailValidationError("No sender specified and no default sender configured")

            message = cls._build_message(params, sender)

            response = cls._client.send(message)

            message_id = response.headers.get("X-Message-Id", "unknown")
            cls._log_email(params, sender, message_id, "sent")

            return {"success": True, "message_id": message_id, "status_code": response.status_code}

        except HTTPError as e:
            error_message = f"SendGrid API error: {str(e)}"
            Logger.error(message=error_message)

            cls._log_email(params, sender or EmailSender(email="unknown", name=None), "failed", "failed", error=str(e))

            raise EmailAPIError(error_message, details={"api_response": str(e)})

        except Exception as e:
            error_message = f"Failed to send email: {str(e)}"
            Logger.error(message=error_message)

            if "sender" in locals() and sender:
                cls._log_email(params, sender, "failed", "failed", error=str(e))

            raise EmailServiceError(error_message)

    @classmethod
    def _process_recipients(cls, recipient_data) -> List[To]:
        """
        Process recipient data into SendGrid To objects

        Args:
            recipient_data: Single EmailRecipient or list of EmailRecipients

        Returns:
            List of SendGrid To objects

        Raises:
            EmailValidationError: If recipient format is invalid
        """
        to_emails = []
        if isinstance(recipient_data, EmailRecipient):
            to_emails.append(To(recipient_data.email, recipient_data.name))
        elif isinstance(recipient_data, list):
            for recipient in recipient_data:
                to_emails.append(To(recipient.email, recipient.name))
        else:
            raise EmailValidationError("Invalid recipient format")
        return to_emails

    @classmethod
    def _create_template_mail(cls, from_email: Email, to_emails: List[To], params: SendEmailParams) -> Mail:
        """
        Create a SendGrid Mail object using a template

        Args:
            from_email: SendGrid Email object for sender
            to_emails: List of SendGrid To objects for recipients
            params: Email parameters

        Returns:
            SendGrid Mail object configured with template
        """
        mail = Mail(from_email=from_email, to_emails=to_emails)
        mail.template_id = params.content.template_id

        if params.content.template_data:
            mail.dynamic_template_data = DynamicTemplateData(params.content.template_data)

        return mail

    @classmethod
    def _create_content_mail(cls, from_email: Email, to_emails: List[To], params: SendEmailParams) -> Mail:
        """
        Create a SendGrid Mail object with content

        Args:
            from_email: SendGrid Email object for sender
            to_emails: List of SendGrid To objects for recipients
            params: Email parameters

        Returns:
            SendGrid Mail object configured with content
        """
        content_type = "text/html" if params.content.is_html else "text/plain"
        content = Content(content_type, params.content.body)

        mail = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject=params.content.subject,
            html_content=content if params.content.is_html else None,
            plain_text_content=None if params.content.is_html else content,
        )

        return mail

    @classmethod
    def _add_cc_recipients(cls, mail: Mail, cc_recipients: List[EmailRecipient]) -> None:
        """
        Add CC recipients to mail object

        Args:
            mail: SendGrid Mail object
            cc_recipients: List of CC recipients
        """
        if not cc_recipients:
            return

        for cc_recipient in cc_recipients:
            mail.cc = Cc(cc_recipient.email, cc_recipient.name)

    @classmethod
    def _add_bcc_recipients(cls, mail: Mail, bcc_recipients: List[EmailRecipient]) -> None:
        """
        Add BCC recipients to mail object

        Args:
            mail: SendGrid Mail object
            bcc_recipients: List of BCC recipients
        """
        if not bcc_recipients:
            return

        for bcc_recipient in bcc_recipients:
            mail.bcc = Bcc(bcc_recipient.email, bcc_recipient.name)

    @classmethod
    def _add_attachments(cls, mail: Mail, attachments: List[Dict[str, str]]) -> None:
        """
        Add attachments to mail object

        Args:
            mail: SendGrid Mail object
            attachments: List of attachment data dictionaries
        """
        if not attachments:
            return

        for attachment_data in attachments:
            attachment = Attachment()
            attachment.file_content = FileContent(attachment_data.get("content", ""))
            attachment.file_name = FileName(attachment_data.get("filename", "attachment"))
            attachment.file_type = FileType(attachment_data.get("type", "application/octet-stream"))
            attachment.disposition = Disposition(attachment_data.get("disposition", "attachment"))
            mail.add_attachment(attachment)

    @classmethod
    def _build_message(cls, params: SendEmailParams, sender: EmailSender) -> Mail:
        """
        Build SendGrid Mail object from parameters

        Args:
            params: Email parameters
            sender: Email sender

        Returns:
            SendGrid Mail object ready to send

        Raises:
            EmailValidationError: If email data is invalid
        """
        try:
            from_email = Email(sender.email, sender.name)

            to_emails = cls._process_recipients(params.to)

            if params.content.template_id:
                mail = cls._create_template_mail(from_email, to_emails, params)
            else:
                mail = cls._create_content_mail(from_email, to_emails, params)

            cls._add_cc_recipients(mail, params.cc)
            cls._add_bcc_recipients(mail, params.bcc)

            if params.reply_to:
                mail.reply_to = ReplyTo(params.reply_to.email, params.reply_to.name)

            cls._add_attachments(mail, params.content.attachments)

            return mail

        except Exception as e:
            raise EmailValidationError(f"Error building email message: {str(e)}")

    @classmethod
    def _prepare_recipient_data(cls, params: SendEmailParams) -> List[Dict[str, str]]:
        """
        Extract recipient information from email parameters for logging

        Args:
            params: Email parameters

        Returns:
            List of recipient data dictionaries
        """
        recipient_emails = []

        if isinstance(params.to, EmailRecipient):
            recipient_emails.append({"email": params.to.email, "name": params.to.name})
        else:
            for recipient in params.to:
                recipient_emails.append({"email": recipient.email, "name": recipient.name})

        if params.cc:
            for cc in params.cc:
                recipient_emails.append({"email": cc.email, "name": cc.name, "type": "cc"})

        if params.bcc:
            for bcc in params.bcc:
                recipient_emails.append({"email": bcc.email, "name": bcc.name, "type": "bcc"})

        return recipient_emails

    @classmethod
    def _determine_content_type(cls, params: SendEmailParams) -> str:
        """
        Determine the content type for logging

        Args:
            params: Email parameters

        Returns:
            Content type string
        """
        if params.content.template_id:
            return "template"
        return "html" if params.content.is_html else "text"

    @classmethod
    def _get_body_content(cls, params: SendEmailParams) -> str:
        """
        Get the body content for logging

        Args:
            params: Email parameters

        Returns:
            Body content or template ID information
        """
        if params.content.template_id:
            return f"Template ID: {params.content.template_id}"
        return params.content.body

    @classmethod
    def _log_email(
        cls, params: SendEmailParams, sender: EmailSender, message_id: str, status: str, error: Optional[str] = None
    ) -> None:
        """
        Log email to database for tracking and auditing

        Args:
            params: Email parameters
            sender: Email sender
            message_id: Message ID from provider
            status: Current status of the email (sent, failed, etc.)
            error: Optional error message if email failed
        """
        try:
            now = datetime.now()

            recipient_emails = cls._prepare_recipient_data(params)

            content_type = cls._determine_content_type(params)

            body = cls._get_body_content(params)

            log_entry = EmailLogModel(
                id=None,
                message_id=message_id,
                sender_email=sender.email,
                sender_name=sender.name,
                recipient_emails=recipient_emails,
                subject=params.content.subject,
                body=body,
                content_type=content_type,
                status=status,
                error=error,
                created_at=now,
                updated_at=now,
            )

            EmailLogRepository.collection().insert_one(log_entry.to_bson())

        except Exception as e:
            Logger.error(message=f"Failed to log email: {str(e)}")
