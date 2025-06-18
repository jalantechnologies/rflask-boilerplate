from typing import Any, Dict, List, Optional, Union

from modules.email_notification.internal.sendgrid_email_provider import SendGridEmailProvider
from modules.email_notification.types import EmailContent, EmailRecipient, EmailSender, SendEmailParams
from modules.logger.logger import Logger


class EmailService:
    """
    Service responsible for sending emails to recipients.
    Acts as a facade to abstract different email provider implementation details.
    """

    _initialized = False

    @staticmethod
    def send_email(*, params: SendEmailParams) -> Dict[str, Any]:
        """
        Sends an email using the configured email provider.

        This method abstracts the underlying email provider (SendGrid)
        to maintain a consistent interface if additional providers are added later.

        Args:
            params: Contains recipient information and email content

        Returns:
            Response containing success status and message ID or error details
        """
        try:
            return SendGridEmailProvider.send_email(params)
        except Exception as e:
            Logger.error(message=f"Error in email service: {str(e)}")
            return {"success": False, "error": "Email service error", "message": str(e)}

    @staticmethod
    def initialize() -> bool:
        """
        Initializes the email service and its providers.

        Should be called during application startup to ensure the
        email infrastructure is ready before handling requests.

        Returns:
            True if initialization was successful, False otherwise
        """
        try:
            SendGridEmailProvider.initialize()
            EmailService._initialized = True
            return True
        except Exception as e:
            Logger.error(message=f"Failed to initialize email service: {str(e)}")
            return False

    @staticmethod
    def send_simple_email(
        to: Union[str, List[str]],
        subject: str,
        body: str,
        is_html: bool = False,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Sends a simple email with text or HTML body.

        This is a convenience method that constructs the necessary objects
        from simple parameters and then calls the main send_email method.

        Args:
            to: Recipient email or list of recipient emails
            subject: Email subject
            body: Email body
            is_html: Whether the body is HTML (default: False)
            from_email: Sender email (uses default if not provided)
            from_name: Sender name (uses default if not provided)
            cc: List of CC recipient emails
            bcc: List of BCC recipient emails

        Returns:
            Response containing success status and message ID or error details
        """
        recipients: Union[EmailRecipient, List[EmailRecipient]]
        if isinstance(to, str):
            recipients = EmailRecipient(email=to)
        elif isinstance(to, list):
            recipients = [EmailRecipient(email=email) for email in to]
        else:
            recipients = []

        sender = None
        if from_email:
            sender = EmailSender(email=from_email, name=from_name)

        cc_recipients = None
        if cc:
            cc_recipients = [EmailRecipient(email=email) for email in cc]

        bcc_recipients = None
        if bcc:
            bcc_recipients = [EmailRecipient(email=email) for email in bcc]

        content = EmailContent(subject=subject, body=body, is_html=is_html)

        params = SendEmailParams(to=recipients, content=content, sender=sender, cc=cc_recipients, bcc=bcc_recipients)

        return EmailService.send_email(params=params)

    @staticmethod
    def send_template_email(
        to: Union[str, List[str]],
        template_id: str,
        template_data: Dict[str, str],
        subject: str = "",
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Sends an email using a SendGrid template.

        This is a convenience method for sending template-based emails
        that automatically constructs the necessary objects.

        Args:
            to: Recipient email or list of recipient emails
            template_id: SendGrid template ID
            template_data: Data to be used in the template
            subject: Email subject (optional for templates)
            from_email: Sender email (uses default if not provided)
            from_name: Sender name (uses default if not provided)
            cc: List of CC recipient emails
            bcc: List of BCC recipient emails

        Returns:
            Response containing success status and message ID or error details
        """
        recipients: Union[EmailRecipient, List[EmailRecipient]]
        if isinstance(to, str):
            recipients = EmailRecipient(email=to)
        elif isinstance(to, list):
            recipients = [EmailRecipient(email=email) for email in to]
        else:
            recipients = []

        sender = None
        if from_email:
            sender = EmailSender(email=from_email, name=from_name)

        cc_recipients = None
        if cc:
            cc_recipients = [EmailRecipient(email=email) for email in cc]

        bcc_recipients = None
        if bcc:
            bcc_recipients = [EmailRecipient(email=email) for email in bcc]

        content = EmailContent(
            subject=subject, body="", is_html=True, template_id=template_id, template_data=template_data
        )

        params = SendEmailParams(to=recipients, content=content, sender=sender, cc=cc_recipients, bcc=bcc_recipients)

        return EmailService.send_email(params=params)
