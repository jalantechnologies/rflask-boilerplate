# src/apps/backend/modules/notification/internals/sendgrid_service.py
from typing import Optional

import sendgrid
from sendgrid.helpers.mail import Content, From, Mail, Personalization, Subject, TemplateId, To

from modules.config.config_service import ConfigService
from modules.notification.errors import ServiceError
from modules.notification.internals.sendgrid_email_params import EmailParams
from modules.notification.types import BulkEmailParams, EmailResponse, SendEmailParams


class SendGridService:
    __client: Optional[sendgrid.SendGridAPIClient] = None

    @staticmethod
    def send_email(params: SendEmailParams) -> EmailResponse:
        """Send email to single or multiple recipients"""
        EmailParams.validate(params)

        try:
            client = SendGridService.get_client()

            if len(params.recipients) == 1:
                # Single recipient email
                response = SendGridService._send_single_email(client, params)
            else:
                # Multiple recipients email
                response = SendGridService._send_bulk_email(client, params)

            return EmailResponse(
                success=True,
                message_id=response.body.get("message_id") if hasattr(response, "body") else None,
                status_code=response.status_code,
            )

        except sendgrid.SendGridException as err:
            return EmailResponse(success=False, status_code=getattr(err, "status_code", 500), errors=[str(err)])
        except Exception as err:
            raise ServiceError(err)

    @staticmethod
    def send_bulk_email(params: BulkEmailParams) -> EmailResponse:
        """Send personalized bulk emails using templates"""
        try:
            client = SendGridService.get_client()

            mail = Mail()
            mail.from_email = From(params.sender.email, params.sender.name)
            mail.template_id = TemplateId(params.template_id)

            # Add personalizations for each recipient
            for i, recipient in enumerate(params.recipients):
                personalization = Personalization()
                personalization.add_to(To(recipient.email, recipient.name))

                # Add personalized template data if provided
                if params.personalizations and i < len(params.personalizations):
                    for key, value in params.personalizations[i].items():
                        personalization.dynamic_template_data = params.personalizations[i]

                mail.add_personalization(personalization)

            response = client.send(mail)

            return EmailResponse(
                success=True,
                message_id=response.body.get("message_id") if hasattr(response, "body") else None,
                status_code=response.status_code,
            )

        except sendgrid.SendGridException as err:
            return EmailResponse(success=False, status_code=getattr(err, "status_code", 500), errors=[str(err)])
        except Exception as err:
            raise ServiceError(err)

    @staticmethod
    def _send_single_email(client: sendgrid.SendGridAPIClient, params: SendEmailParams) -> any:
        """Send email to a single recipient"""
        recipient = params.recipients[0]

        mail = Mail(
            from_email=From(params.sender.email, params.sender.name), to_emails=To(recipient.email, recipient.name)
        )

        if params.template_id:
            # Template-based email
            mail.template_id = TemplateId(params.template_id)
            if params.template_data:
                mail.dynamic_template_data = params.template_data
        else:
            # Direct content email
            if params.subject:
                mail.subject = Subject(params.subject)
            if params.html_content:
                mail.add_content(Content("text/html", params.html_content))
            if params.text_content:
                mail.add_content(Content("text/plain", params.text_content))

        return client.send(mail)

    @staticmethod
    def _send_bulk_email(client: sendgrid.SendGridAPIClient, params: SendEmailParams) -> any:
        """Send the same email to multiple recipients"""
        mail = Mail()
        mail.from_email = From(params.sender.email, params.sender.name)

        # Create a single personalization for all recipients
        personalization = Personalization()
        for recipient in params.recipients:
            personalization.add_to(To(recipient.email, recipient.name))

        if params.template_id:
            # Template-based email
            mail.template_id = TemplateId(params.template_id)
            if params.template_data:
                personalization.dynamic_template_data = params.template_data
        else:
            # Direct content email
            if params.subject:
                mail.subject = Subject(params.subject)
            if params.html_content:
                mail.add_content(Content("text/html", params.html_content))
            if params.text_content:
                mail.add_content(Content("text/plain", params.text_content))

        mail.add_personalization(personalization)
        return client.send(mail)

    @staticmethod
    def get_client() -> sendgrid.SendGridAPIClient:
        if not SendGridService.__client:
            api_key = ConfigService[str].get_value(key="sendgrid.api_key")
            SendGridService.__client = sendgrid.SendGridAPIClient(api_key=api_key)
        return SendGridService.__client

    @staticmethod
    def get_default_sender() -> tuple[str, str]:
        """Get default sender email and name from configuration"""
        try:
            default_email = ConfigService[str].get_value(key="mailer.default_email", default="noreply@example.com")
            default_name = ConfigService[str].get_value(key="mailer.default_email_name", default="No Reply")

            # Ensure we don't return placeholder values
            if default_email in ["DEFAULT_EMAIL", "MAILER_DEFAULT_EMAIL"]:
                default_email = "noreply@example.com"
            if default_name in ["DEFAULT_EMAIL_NAME", "MAILER_DEFAULT_EMAIL_NAME"]:
                default_name = "No Reply"

            return default_email, default_name
        except Exception:
            # Fallback to safe defaults if configuration fails
            return "noreply@example.com", "No Reply"
