import json
from typing import Optional

import sendgrid
from sendgrid.helpers.mail import Content, From, Mail, Personalization, Subject, TemplateId, To

from modules.config.config_service import ConfigService
from modules.config.errors import MissingKeyError
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
                response = SendGridService._send_single_email(client, params)
            else:
                response = SendGridService._send_bulk_email(client, params)

            message_id = SendGridService._extract_message_id(response)

            return EmailResponse(success=True, message_id=message_id, status_code=response.status_code)

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

            for i, recipient in enumerate(params.recipients):
                personalization = Personalization()

                if recipient.name:
                    personalization.add_to(To(recipient.email, recipient.name))
                else:
                    personalization.add_to(To(recipient.email))

                if params.personalizations and i < len(params.personalizations):
                    personalization.dynamic_template_data = params.personalizations[i]

                mail.add_personalization(personalization)

            response = client.send(mail)

            message_id = SendGridService._extract_message_id(response)

            return EmailResponse(success=True, message_id=message_id, status_code=response.status_code)

        except sendgrid.SendGridException as err:
            return EmailResponse(success=False, status_code=getattr(err, "status_code", 500), errors=[str(err)])
        except Exception as err:
            raise ServiceError(err)

    @staticmethod
    def _send_single_email(client: sendgrid.SendGridAPIClient, params: SendEmailParams) -> any:
        """Send email to a single recipient"""
        recipient = params.recipients[0]

        if recipient.name:
            to_email = To(recipient.email, recipient.name)
        else:
            to_email = To(recipient.email)

        mail = Mail(from_email=From(params.sender.email, params.sender.name), to_emails=to_email)

        if params.template_id:
            mail.template_id = TemplateId(params.template_id)
            if params.template_data:
                mail.dynamic_template_data = params.template_data
        else:
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

        personalization = Personalization()
        for recipient in params.recipients:
            if recipient.name:
                personalization.add_to(To(recipient.email, recipient.name))
            else:
                personalization.add_to(To(recipient.email))

        if params.template_id:
            mail.template_id = TemplateId(params.template_id)
            if params.template_data:
                personalization.dynamic_template_data = params.template_data
        else:
            if params.subject:
                mail.subject = Subject(params.subject)
            if params.html_content:
                mail.add_content(Content("text/html", params.html_content))
            if params.text_content:
                mail.add_content(Content("text/plain", params.text_content))

        mail.add_personalization(personalization)
        return client.send(mail)

    @staticmethod
    def _extract_message_id(response) -> Optional[str]:
        """Extract message ID from SendGrid response"""
        try:
            if hasattr(response, "headers") and response.headers:
                if isinstance(response.headers, str):
                    for line in response.headers.split("\n"):
                        if line.startswith("X-Message-Id:"):
                            return line.split(":", 1)[1].strip()
                elif hasattr(response.headers, "get"):
                    return response.headers.get("X-Message-Id")

            if hasattr(response, "body") and response.body:
                if isinstance(response.body, bytes):
                    try:
                        body_str = response.body.decode("utf-8")
                        if body_str.strip():  # Only parse if not empty
                            body_dict = json.loads(body_str)
                            return body_dict.get("message_id")
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        pass
                elif isinstance(response.body, dict):
                    return response.body.get("message_id")
                elif hasattr(response.body, "get"):
                    return response.body.get("message_id")

            return None

        except Exception:
            return None

    @staticmethod
    def get_client() -> sendgrid.SendGridAPIClient:
        if not SendGridService.__client:
            try:
                api_key = ConfigService[str].get_value(key="sendgrid.api_key")
                SendGridService.__client = sendgrid.SendGridAPIClient(api_key=api_key)
            except MissingKeyError:
                raise ServiceError("SendGrid API key not found in configuration")
        return SendGridService.__client

    @staticmethod
    def get_default_sender() -> tuple[str, str]:
        """Get default sender email and name from configuration"""
        try:
            try:
                default_email = ConfigService[str].get_value(key="mailer.default_email")
            except MissingKeyError:
                default_email = "noreply@example.com"

            try:
                default_name = ConfigService[str].get_value(key="mailer.default_email_name")
            except MissingKeyError:
                default_name = "No Reply"

            if default_email in ["DEFAULT_EMAIL", "MAILER_DEFAULT_EMAIL", ""]:
                default_email = "noreply@example.com"
            if default_name in ["DEFAULT_EMAIL_NAME", "MAILER_DEFAULT_EMAIL_NAME", ""]:
                default_name = "No Reply"

            return default_email, default_name
        except Exception:
            return "noreply@example.com", "No Reply"
