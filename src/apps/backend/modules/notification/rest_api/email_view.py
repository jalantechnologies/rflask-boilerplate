import logging
from typing import Any, Dict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.notification.email_service import EmailService
from modules.notification.types import EmailRecipient, EmailSender, SendEmailParams

logger = logging.getLogger(__name__)


class EmailView(MethodView):
    def post(self) -> ResponseReturnValue:
        """
        Send emails via multiple methods:
        1. Simple email (single or multiple recipients):
        {
            "type": "simple",
            "to_emails": ["user1@example.com", "user2@example.com"],
            "subject": "Test Email",
            "html_content": "<h1>Hello</h1>",
            "text_content": "Hello",
            "from_email": "sender@example.com",
            "from_name": "Sender Name"
        }
        2. Template email:
        {
            "type": "template",
            "to_emails": ["user1@example.com", "user2@example.com"],
            "template_id": "d-1234567890",
            "template_data": {"name": "John", "product": "Premium"},
            "from_email": "sender@example.com",
            "from_name": "Sender Name"
        }
        3. Personalized bulk email:
        {
            "type": "bulk",
            "template_id": "d-1234567890",
            "recipients_data": [
                {
                    "email": "user1@example.com",
                    "name": "John Doe",
                    "template_data": {"name": "John", "balance": "$100"}
                },
                {
                    "email": "user2@example.com",
                    "name": "Jane Smith",
                    "template_data": {"name": "Jane", "balance": "$200"}
                }
            ],
            "from_email": "sender@example.com",
            "from_name": "Sender Name"
        }
        4. Advanced email (full control):
        {
            "type": "advanced",
            "recipients": [
                {"email": "user1@example.com", "name": "John Doe"},
                {"email": "user2@example.com", "name": "Jane Smith"}
            ],
            "sender": {"email": "sender@example.com", "name": "Sender Name"},
            "template_id": "d-1234567890",       // Optional
            "template_data": {"key": "value"},   // Optional
            "subject": "Email Subject",          // Optional (required for non-template)
            "html_content": "<h1>Content</h1>",  // Optional
            "text_content": "Content"            // Optional
        }
        """

        try:
            request_data = request.get_json()

            if not request_data:
                return jsonify({"error": "Request body is required", "success": False}), 400

            email_type = request_data.get("type", "simple")

            if email_type == "simple":
                response = self._handle_simple_email(request_data)
            elif email_type == "template":
                response = self._handle_template_email(request_data)
            elif email_type == "bulk":
                response = self._handle_bulk_email(request_data)
            elif email_type == "advanced":
                response = self._handle_advanced_email(request_data)
            else:
                return jsonify({"error": f"Invalid email type: {email_type}", "success": False}), 400

            if response.success:
                return (
                    jsonify(
                        {
                            "success": True,
                            "message": "Email sent successfully",
                            "message_id": response.message_id,
                            "status_code": response.status_code,
                        }
                    ),
                    200,
                )
            else:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Failed to send email",
                            "errors": response.errors,
                            "status_code": response.status_code,
                        }
                    ),
                    response.status_code or 500,
                )

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return jsonify({"success": False, "message": "Validation error", "error": str(e)}), 400

        except IndexError:
            logger.exception("Configuration error: tuple index out of range - check email configuration")
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Configuration error",
                        "error": "tuple index out of range - check email configuration",
                    }
                ),
                500,
            )

        except Exception as e:
            logger.exception("Internal server error")
            return jsonify({"success": False, "message": "Internal server error", "error": str(e)}), 500

    def _handle_simple_email(self, data: Dict[str, Any]) -> Any:
        try:
            required_fields = ["to_emails"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")

            if not data.get("template_id"):
                if not data.get("subject"):
                    raise ValueError("Subject is required for non-template emails")
                if not data.get("html_content") and not data.get("text_content"):
                    raise ValueError("Either html_content or text_content is required for non-template emails")

            logger.info(f"Sending simple email to: {data['to_emails']}")

            return EmailService.send_simple_email(
                to_emails=data["to_emails"],
                subject=data.get("subject"),
                html_content=data.get("html_content"),
                text_content=data.get("text_content"),
                from_email=data.get("from_email"),
                from_name=data.get("from_name"),
                template_id=data.get("template_id"),
                template_data=data.get("template_data"),
            )
        except Exception as e:
            logger.exception(f"Error in _handle_simple_email: {e}")
            raise

    def _handle_template_email(self, data: Dict[str, Any]) -> Any:
        try:
            required_fields = ["to_emails", "template_id"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")

            logger.info(f"Sending template email to: {data['to_emails']}")

            return EmailService.send_template_email(
                to_emails=data["to_emails"],
                template_id=data["template_id"],
                template_data=data.get("template_data"),
                from_email=data.get("from_email"),
                from_name=data.get("from_name"),
            )
        except Exception as e:
            logger.exception(f"Error in _handle_template_email: {e}")
            raise

    def _handle_bulk_email(self, data: Dict[str, Any]) -> Any:
        try:
            required_fields = ["recipients_data", "template_id"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")

            logger.info(f"Sending bulk email to {len(data['recipients_data'])} recipients")

            return EmailService.send_personalized_bulk_email(
                recipients_data=data["recipients_data"],
                template_id=data["template_id"],
                from_email=data.get("from_email"),
                from_name=data.get("from_name"),
            )
        except Exception as e:
            logger.exception(f"Error in _handle_bulk_email: {e}")
            raise

    def _handle_advanced_email(self, data: Dict[str, Any]) -> Any:
        try:
            required_fields = ["recipients", "sender"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")

            recipients = [
                EmailRecipient(email=recipient["email"], name=recipient.get("name")) for recipient in data["recipients"]
            ]

            sender_data = data["sender"]
            sender = EmailSender(email=sender_data["email"], name=sender_data["name"])

            logger.info(f"Sending advanced email to {len(recipients)} recipients")

            params = SendEmailParams(
                recipients=recipients,
                sender=sender,
                template_id=data.get("template_id"),
                template_data=data.get("template_data"),
                subject=data.get("subject"),
                html_content=data.get("html_content"),
                text_content=data.get("text_content"),
            )

            return EmailService.send_email(params=params)
        except Exception as e:
            logger.exception(f"Error in _handle_advanced_email: {e}")
            raise
