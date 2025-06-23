from typing import List

from modules.notification.internals.sendgrid_service import SendGridService
from modules.notification.types import BulkEmailParams, EmailRecipient, EmailResponse, EmailSender, SendEmailParams


class EmailService:
    @staticmethod
    def send_email(*, params: SendEmailParams) -> EmailResponse:
        return SendGridService.send_email(params)

    @staticmethod
    def send_bulk_email(*, params: BulkEmailParams) -> EmailResponse:
        return SendGridService.send_bulk_email(params)

    @staticmethod
    def send_simple_email(
        *,
        to_emails: List[str] | str,
        subject: str | None,
        html_content: str | None = None,
        text_content: str | None = None,
        from_email: str | None = None,
        from_name: str | None = None,
        template_id: str | None = None,
        template_data: dict | None = None,
    ) -> EmailResponse:
        try:
            if not from_email or not from_name:
                default_email, default_name = SendGridService.get_default_sender()
                from_email = from_email or default_email
                from_name = from_name or default_name
        except Exception:
            from_email = from_email or "noreply@example.com"
            from_name = from_name or "No Reply"

        if isinstance(to_emails, str):
            to_emails = [to_emails]

        recipients = [EmailRecipient(email=email) for email in to_emails]

        sender = EmailSender(email=from_email, name=from_name)

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
        template_data: dict | None = None,
        from_email: str | None = None,
        from_name: str | None = None,
    ) -> EmailResponse:

        return EmailService.send_simple_email(
            to_emails=to_emails,
            subject=None,  # Now valid since subject parameter accepts None
            template_id=template_id,
            template_data=template_data,
            from_email=from_email,
            from_name=from_name,
        )

    @staticmethod
    def send_personalized_bulk_email(
        *, recipients_data: List[dict], template_id: str, from_email: str | None = None, from_name: str | None = None
    ) -> EmailResponse:
        try:
            if not from_email or not from_name:
                default_email, default_name = SendGridService.get_default_sender()
                from_email = from_email or default_email
                from_name = from_name or default_name
        except Exception:
            from_email = from_email or "noreply@example.com"
            from_name = from_name or "No Reply"

        recipients = []
        personalizations = []

        for recipient_data in recipients_data:
            recipients.append(EmailRecipient(email=recipient_data["email"], name=recipient_data.get("name")))
            personalizations.append(recipient_data.get("template_data", {}))

        sender = EmailSender(email=from_email, name=from_name)

        params = BulkEmailParams(
            recipients=recipients, sender=sender, template_id=template_id, personalizations=personalizations
        )

        return EmailService.send_bulk_email(params=params)
