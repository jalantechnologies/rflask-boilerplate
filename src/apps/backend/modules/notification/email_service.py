# src/apps/backend/modules/notification/email_service.py
from typing import List

from modules.notification.internals.sendgrid_service import SendGridService
from modules.notification.types import BulkEmailParams, EmailRecipient, EmailResponse, EmailSender, SendEmailParams


class EmailService:
    @staticmethod
    def send_email(*, params: SendEmailParams) -> EmailResponse:
        """Send email to single or multiple recipients"""
        return SendGridService.send_email(params)

    @staticmethod
    def send_bulk_email(*, params: BulkEmailParams) -> EmailResponse:
        """Send personalized bulk emails"""
        return SendGridService.send_bulk_email(params)

    @staticmethod
    def send_simple_email(
        *,
        to_emails: List[str] | str,
        subject: str,
        html_content: str = None,
        text_content: str = None,
        from_email: str = None,
        from_name: str = None,
        template_id: str = None,
        template_data: dict = None,
    ) -> EmailResponse:
        """
        Simplified method to send emails without creating complex params objects

        Args:
            to_emails: Single email string or list of email strings
            subject: Email subject (required for non-template emails)
            html_content: HTML content (optional)
            text_content: Plain text content (optional)
            from_email: Sender email (uses default if not provided)
            from_name: Sender name (uses default if not provided)
            template_id: SendGrid template ID (optional)
            template_data: Template variables (optional)
        """

        # Handle default sender info
        if not from_email or not from_name:
            default_email, default_name = SendGridService.get_default_sender()
            from_email = from_email or default_email
            from_name = from_name or default_name

        # Convert single email to list
        if isinstance(to_emails, str):
            to_emails = [to_emails]

        # Create recipients list
        recipients = [EmailRecipient(email=email) for email in to_emails]

        # Create sender
        sender = EmailSender(email=from_email, name=from_name)

        # Create params
        params = SendEmailParams(
            recipients=recipients,
            sender=sender,
            template_id=template_id,
            template_data=template_data,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
        )

        return EmailService.send_email(params=params)

    @staticmethod
    def send_template_email(
        *,
        to_emails: List[str] | str,
        template_id: str,
        template_data: dict = None,
        from_email: str = None,
        from_name: str = None,
    ) -> EmailResponse:
        """
        Send template-based emails

        Args:
            to_emails: Single email string or list of email strings
            template_id: SendGrid template ID
            template_data: Template variables
            from_email: Sender email (uses default if not provided)
            from_name: Sender name (uses default if not provided)
        """

        return EmailService.send_simple_email(
            to_emails=to_emails,
            subject=None,  # Subject comes from template
            template_id=template_id,
            template_data=template_data,
            from_email=from_email,
            from_name=from_name,
        )

    @staticmethod
    def send_personalized_bulk_email(
        *, recipients_data: List[dict], template_id: str, from_email: str = None, from_name: str = None
    ) -> EmailResponse:
        """
        Send personalized emails to multiple recipients with individual template data

        Args:
            recipients_data: List of dicts with 'email', optional 'name', and 'template_data'
                           Example: [{'email': 'user@example.com', 'name': 'John', 'template_data': {'var': 'value'}}]
            template_id: SendGrid template ID
            from_email: Sender email (uses default if not provided)
            from_name: Sender name (uses default if not provided)
        """

        # Handle default sender info
        if not from_email or not from_name:
            default_email, default_name = SendGridService.get_default_sender()
            from_email = from_email or default_email
            from_name = from_name or default_name

        # Create recipients and personalizations
        recipients = []
        personalizations = []

        for recipient_data in recipients_data:
            recipients.append(EmailRecipient(email=recipient_data["email"], name=recipient_data.get("name")))
            personalizations.append(recipient_data.get("template_data", {}))

        # Create sender
        sender = EmailSender(email=from_email, name=from_name)

        # Create params
        params = BulkEmailParams(
            recipients=recipients, sender=sender, template_id=template_id, personalizations=personalizations
        )

        return EmailService.send_bulk_email(params=params)
