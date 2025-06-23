import logging
from typing import Any, Dict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.account.types import PhoneNumber
from modules.notification.sms_service import SMSService
from modules.notification.types import BulkSMSParams, PersonalizedSMSParams, SMSErrorCode

logger = logging.getLogger(__name__)


class SMSView(MethodView):
    def post(self) -> ResponseReturnValue:
        """
        Send SMS via multiple methods:

        1. Simple SMS (single recipient):
        {
            "type": "simple",
            "phone_number": "+1234567890",
            "message": "Your OTP is 123456"
        }

        2. Simple SMS (multiple recipients with same message):
        {
            "type": "simple",
            "phone_numbers": ["+1234567890", "+9876543210"],
            "message": "Server maintenance tonight at 2 AM"
        }

        3. Bulk SMS (multiple recipients):
        {
            "type": "bulk",
            "recipient_phones": [
                {
                    "country_code": "+1",
                    "phone_number": "234567890"
                },
                {
                    "country_code": "+1",
                    "phone_number": "876543210"
                }
            ],
            "message": "Bulk notification message"
        }

        4. Personalized SMS (with templates):
        {
            "type": "personalized",
            "message_template": "Hello {name}, your order #{order_id} is ready for pickup!",
            "recipients_data": [
                {
                    "phone": {
                        "country_code": "+1",
                        "phone_number": "234567890"
                    },
                    "template_data": {
                        "name": "John",
                        "order_id": "12345"
                    }
                },
                {
                    "phone": {
                        "country_code": "+1",
                        "phone_number": "876543210"
                    },
                    "template_data": {
                        "name": "Jane",
                        "order_id": "67890"
                    }
                }
            ]
        }
        """
        try:
            data = request.get_json()

            if not data:
                return (
                    jsonify(
                        {"success": False, "message": "Request body is required", "code": SMSErrorCode.VALIDATION_ERROR}
                    ),
                    400,
                )

            sms_type = data.get("type", "simple")

            if sms_type == "simple":
                result = self._handle_simple_sms(data)
            elif sms_type == "bulk":
                result = self._handle_bulk_sms(data)
            elif sms_type == "personalized":
                result = self._handle_personalized_sms(data)
            else:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": f"Unsupported SMS type: {sms_type}. Supported types: simple, bulk, personalized",
                            "code": SMSErrorCode.VALIDATION_ERROR,
                        }
                    ),
                    400,
                )

            response_data = {
                "success": result.success,
                "sent_count": result.sent_count,
                "failed_count": result.failed_count,
                "message_ids": result.message_ids,
                "errors": result.errors,
            }

            status_code = 200 if result.success else 400
            return jsonify(response_data), status_code

        except ValueError as e:
            logger.error(f"Validation error in SMS API: {e}")
            return jsonify({"success": False, "message": str(e), "code": SMSErrorCode.VALIDATION_ERROR}), 400
        except Exception as e:
            logger.exception(f"Unexpected error in SMS API: {e}")
            return (
                jsonify({"success": False, "message": "Internal server error", "code": SMSErrorCode.SERVICE_ERROR}),
                500,
            )

    def _handle_simple_sms(self, data: Dict[str, Any]) -> Any:
        try:
            message = data.get("message")
            if not message:
                raise ValueError("Message is required")

            if "phone_number" in data:
                phone_number = data["phone_number"]
                return SMSService.send_simple_sms(phone_numbers=phone_number, message=message)

            elif "phone_numbers" in data:
                phone_numbers = data["phone_numbers"]
                if not isinstance(phone_numbers, list):
                    raise ValueError("phone_numbers must be a list")

                return SMSService.send_simple_sms(phone_numbers=phone_numbers, message=message)

            else:
                raise ValueError("Either 'phone_number' or 'phone_numbers' is required")

        except Exception as e:
            logger.exception(f"Error in _handle_simple_sms: {e}")
            raise

    def _handle_bulk_sms(self, data: Dict[str, Any]) -> Any:
        try:
            required_fields = ["recipient_phones", "message"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")

            recipient_phones = []
            for phone_data in data["recipient_phones"]:
                if isinstance(phone_data, dict):
                    phone_number = PhoneNumber(
                        country_code=phone_data.get("country_code", "+1"), phone_number=phone_data.get("phone_number")
                    )
                    recipient_phones.append(phone_number)
                else:
                    raise ValueError("Each recipient_phone must be an object with country_code and phone_number")

            logger.info(f"Sending bulk SMS to {len(recipient_phones)} recipients")

            params = BulkSMSParams(message_body=data["message"], recipient_phones=recipient_phones)

            return SMSService.send_bulk_sms(params=params)

        except Exception as e:
            logger.exception(f"Error in _handle_bulk_sms: {e}")
            raise

    def _handle_personalized_sms(self, data: Dict[str, Any]) -> Any:
        try:
            required_fields = ["message_template", "recipients_data"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")

            processed_recipients = []
            for recipient in data["recipients_data"]:
                phone_data = recipient.get("phone")
                if not phone_data:
                    raise ValueError("Each recipient must have a 'phone' field")

                if isinstance(phone_data, dict):
                    phone_number = PhoneNumber(
                        country_code=phone_data.get("country_code", "+1"), phone_number=phone_data.get("phone_number")
                    )
                elif isinstance(phone_data, str):
                    if phone_data.startswith("+"):
                        phone_number = PhoneNumber(country_code=phone_data[:3], phone_number=phone_data[3:])
                    else:
                        phone_number = PhoneNumber(country_code="+1", phone_number=phone_data)
                else:
                    phone_number = phone_data

                processed_recipients.append(
                    {"phone": phone_number, "template_data": recipient.get("template_data", {})}
                )

            logger.info(f"Sending personalized SMS to {len(processed_recipients)} recipients")

            params = PersonalizedSMSParams(
                message_template=data["message_template"], recipients_data=processed_recipients
            )

            return SMSService.send_personalized_sms(params=params)

        except Exception as e:
            logger.exception(f"Error in _handle_personalized_sms: {e}")
            raise
