import json
from typing import Any, Optional

import sendgrid
from sendgrid.helpers.mail import Content, From, Mail, Personalization, Subject, TemplateId, To

from modules.config.config_service import ConfigService
from modules.config.errors import MissingKeyError
from modules.notification.errors import ServiceError
from modules.notification.internals.sendgrid_email_params import EmailParams
from modules.notification.types import BulkEmailParams, EmailResponse, SendEmailParams

_DEFAULT_EMAIL = "noreply@example.com"
_DEFAULT_NAME = "No Reply"
_INVALID_EMAIL_LITERALS = {"DEFAULT_EMAIL", "MAILER_DEFAULT_EMAIL", ""}
_INVALID_NAME_LITERALS = {"DEFAULT_EMAIL_NAME", "MAILER_DEFAULT_EMAIL_NAME", ""}


class SendGridService:
    __client: Optional[sendgrid.SendGridAPIClient] = None

    @staticmethod
    def send_email(params: SendEmailParams) -> EmailResponse:
        EmailParams.validate(params)
        try:
            client = SendGridService.get_client()
            if len(params.recipients) == 1:
                response = SendGridService._send_single_email(client, params)
            else:
                response = SendGridService._send_bulk_email(client, params)

            message_id = SendGridService._extract_message_id(response)
            status_code = getattr(response, "status_code", None)
            return EmailResponse(success=True, message_id=message_id, status_code=status_code)

        except sendgrid.SendGridException as err:
            return EmailResponse(success=False, status_code=getattr(err, "status_code", 500), errors=[str(err)])
        except Exception as err:
            raise ServiceError(err)

    @staticmethod
    def send_bulk_email(params: BulkEmailParams) -> EmailResponse:
        try:
            client = SendGridService.get_client()
            mail = Mail()
            mail.from_email = From(params.sender.email, params.sender.name)
            mail.template_id = TemplateId(params.template_id)

            for idx, recipient in enumerate(params.recipients):
                personalization = Personalization()
                to = To(recipient.email, recipient.name) if recipient.name else To(recipient.email)
                personalization.add_to(to)

                if params.personalizations and idx < len(params.personalizations):
                    personalization.dynamic_template_data = params.personalizations[idx]

                mail.add_personalization(personalization)

            response = client.send(mail)
            message_id = SendGridService._extract_message_id(response)
            status_code = getattr(response, "status_code", None)
            return EmailResponse(success=True, message_id=message_id, status_code=status_code)

        except sendgrid.SendGridException as err:
            return EmailResponse(success=False, status_code=getattr(err, "status_code", 500), errors=[str(err)])
        except Exception as err:
            raise ServiceError(err)

    @staticmethod
    def _send_single_email(client: sendgrid.SendGridAPIClient, params: SendEmailParams) -> Any:
        recipient = params.recipients[0]
        to_email = To(recipient.email, recipient.name) if recipient.name else To(recipient.email)
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
    def _send_bulk_email(client: sendgrid.SendGridAPIClient, params: SendEmailParams) -> Any:
        mail = Mail()
        mail.from_email = From(params.sender.email, params.sender.name)
        personalization = Personalization()

        for recipient in params.recipients:
            to = To(recipient.email, recipient.name) if recipient.name else To(recipient.email)
            personalization.add_to(to)

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
    def _extract_message_id(response: Any) -> Optional[str]:
        try:
            message_id = SendGridService._extract_from_headers(response)
            if message_id:
                return message_id

            return SendGridService._extract_from_body(response)

        except Exception:
            return None

    @staticmethod
    def _extract_from_headers(response: Any) -> Optional[str]:
        headers = getattr(response, "headers", None)
        if not headers:
            return None

        if isinstance(headers, str):
            return SendGridService._parse_string_headers(headers)
        elif hasattr(headers, "get"):
            return headers.get("X-Message-Id")

        return None

    @staticmethod
    def _parse_string_headers(headers: str) -> Optional[str]:
        for line in headers.splitlines():
            if line.lower().startswith("x-message-id:"):
                return line.split(":", 1)[1].strip()
        return None

    @staticmethod
    def _extract_from_body(response: Any) -> Optional[str]:
        body = getattr(response, "body", None)
        if not body:
            return None

        if isinstance(body, bytes):
            return SendGridService._parse_bytes_body(body)
        elif isinstance(body, dict):
            return body.get("message_id")
        elif hasattr(body, "get"):
            return body.get("message_id")

        return None

    @staticmethod
    def _parse_bytes_body(body: bytes) -> Optional[str]:
        try:
            decoded = body.decode("utf-8")
            data = json.loads(decoded)
            return data.get("message_id")
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

    @staticmethod
    def get_client() -> sendgrid.SendGridAPIClient:
        if not SendGridService.__client:
            try:
                api_key = ConfigService[str].get_value(key="sendgrid.api_key")
                SendGridService.__client = sendgrid.SendGridAPIClient(api_key=api_key)
            except MissingKeyError:
                raise ServiceError(Exception("SendGrid API key not found in configuration"))
        return SendGridService.__client

    @staticmethod
    def get_default_sender() -> tuple[str, str]:
        email = _DEFAULT_EMAIL
        name = _DEFAULT_NAME

        try:
            cfg_email = ConfigService[str].get_value(key="mailer.default_email")
            if cfg_email and cfg_email not in _INVALID_EMAIL_LITERALS:
                email = cfg_email
        except MissingKeyError:
            pass

        try:
            cfg_name = ConfigService[str].get_value(key="mailer.default_email_name")
            if cfg_name and cfg_name not in _INVALID_NAME_LITERALS:
                name = cfg_name
        except MissingKeyError:
            pass

        return email, name
