from typing import Any, Dict, List, Optional, Union

from flask import request
from flask.views import MethodView

from modules.email_notification.email_service import EmailService
from modules.email_notification.errors import EmailError
from modules.email_notification.types import EmailContent, EmailRecipient, EmailSender, SendEmailParams
from modules.logger.logger import Logger


class EmailView(MethodView):
    """View handling email-related API requests"""

    def post(self) -> tuple[Dict[str, Any], int]:
        """
        Handle POST request to send an email

        Expects JSON body with email details:
        {
            "to": "recipient@example.com" | [{"email": "user@example.com", "name": "User Name"}],
            "subject": "Email subject",
            "body": "Email body content",
            "is_html": true|false,
            "from": {"email": "sender@example.com", "name": "Sender Name"} (optional),
            "cc": [{"email": "cc@example.com", "name": "CC Recipient"}] (optional),
            "bcc": [{"email": "bcc@example.com", "name": "BCC Recipient"}] (optional),
            "reply_to": {"email": "reply@example.com", "name": "Reply Name"} (optional)
        }

        For template emails (when route is /emails/template):
        {
            "to": "recipient@example.com" | [{"email": "user@example.com", "name": "User Name"}],
            "template_id": "d-f3ecde555eee47a1b1460aa58c9c57e9",
            "template_data": {"name": "John", "company": "Example Inc"},
            "subject": "Email subject" (optional, as it may be part of template),
            "from": {"email": "sender@example.com", "name": "Sender Name"} (optional),
            "cc": [{"email": "cc@example.com", "name": "CC Recipient"}] (optional),
            "bcc": [{"email": "bcc@example.com", "name": "BCC Recipient"}] (optional),
            "reply_to": {"email": "reply@example.com", "name": "Reply Name"} (optional)
        }

        Returns:
            Tuple of (response_dict, status_code)
        """
        try:
            data = request.get_json()

            if not data:
                return {"error": "Missing request body"}, 400

            is_template = "template_id" in data or request.path.endswith("/template")

            if is_template:
                return self._handle_template_email(data)
            else:
                return self._handle_regular_email(data)

        except EmailError as e:
            Logger.error(message=f"Email API error: {str(e)}")
            return {"success": False, "code": e.code, "message": str(e), "details": e.details}, 400

        except Exception as e:
            Logger.error(message=f"Unexpected error in email API: {str(e)}")
            return {"success": False, "error": "Internal server error"}, 500

    def _handle_regular_email(self, data: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
        """
        Process a regular email request

        Args:
            data: Request data

        Returns:
            Tuple of (response_dict, status_code)
        """
        if "to" not in data:
            return {"error": "Missing required field: to"}, 400
        if "subject" not in data:
            return {"error": "Missing required field: subject"}, 400
        if "body" not in data:
            return {"error": "Missing required field: body"}, 400

        to_recipients = self._process_recipients(data["to"])

        from_sender = self._process_sender(data.get("from"))
        cc_recipients = self._process_recipients(data.get("cc", []))
        bcc_recipients = self._process_recipients(data.get("bcc", []))
        reply_to = self._process_sender(data.get("reply_to"))

        content = EmailContent(subject=data["subject"], body=data["body"], is_html=data.get("is_html", False))

        params = SendEmailParams(
            to=to_recipients,
            content=content,
            sender=from_sender,
            cc=cc_recipients if cc_recipients else None,
            bcc=bcc_recipients if bcc_recipients else None,
            reply_to=reply_to,
        )

        result = EmailService.send_email(params=params)

        if result.get("success", False):
            return result, 200
        else:
            return result, 400

    def _handle_template_email(self, data: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
        """
        Process a template email request

        Args:
            data: Request data

        Returns:
            Tuple of (response_dict, status_code)
        """
        if "to" not in data:
            return {"error": "Missing required field: to"}, 400
        if "template_id" not in data:
            return {"error": "Missing required field: template_id"}, 400
        if "template_data" not in data:
            return {"error": "Missing required field: template_data"}, 400

        to_recipients = self._process_recipients(data["to"])

        from_sender = self._process_sender(data.get("from"))
        cc_recipients = self._process_recipients(data.get("cc", []))
        bcc_recipients = self._process_recipients(data.get("bcc", []))
        reply_to = self._process_sender(data.get("reply_to"))

        content = EmailContent(
            subject=data.get("subject", ""),
            body="",
            is_html=True,
            template_id=data["template_id"],
            template_data=data["template_data"],
        )

        params = SendEmailParams(
            to=to_recipients,
            content=content,
            sender=from_sender,
            cc=cc_recipients if cc_recipients else None,
            bcc=bcc_recipients if bcc_recipients else None,
            reply_to=reply_to,
        )

        result = EmailService.send_email(params=params)

        if result.get("success", False):
            return result, 200
        else:
            return result, 400

    def _process_recipients(
        self, recipients_data: Union[str, List[Dict[str, str]], None]
    ) -> Union[EmailRecipient, List[EmailRecipient]]:
        """
        Process recipient data into EmailRecipient objects

        Args:
            recipients_data: String email, list of emails, or list of email objects

        Returns:
            Single EmailRecipient or list of EmailRecipients
        """
        if not recipients_data:
            return []

        if isinstance(recipients_data, str):
            return EmailRecipient(email=recipients_data)

        if isinstance(recipients_data, list):
            result = []
            for item in recipients_data:
                if isinstance(item, str):
                    result.append(EmailRecipient(email=item))
                elif isinstance(item, dict) and "email" in item:
                    result.append(EmailRecipient(email=item["email"], name=item.get("name")))
            return result

        if isinstance(recipients_data, dict) and "email" in recipients_data:
            return EmailRecipient(email=recipients_data["email"], name=recipients_data.get("name"))

        return []

    def _process_sender(self, sender_data: Optional[Dict[str, str]]) -> Optional[EmailSender]:
        """
        Process sender data into EmailSender object

        Args:
            sender_data: Dictionary with email and name

        Returns:
            EmailSender or None
        """
        if not sender_data:
            return None

        if isinstance(sender_data, dict) and "email" in sender_data:
            return EmailSender(email=sender_data["email"], name=sender_data.get("name"))

        return None
