from typing import Any, Dict, Tuple

from flask import request
from flask.views import MethodView

from modules.account.types import PhoneNumber
from modules.logger.logger import Logger
from modules.sms_notification.errors import SMSNotificationError, ValidationError
from modules.sms_notification.sms_service import SMSNotificationService
from modules.sms_notification.types import SendSMSParams


class SMSNotificationView(MethodView):
    """View for handling SMS notification API requests"""

    def post(self) -> Tuple[Dict[str, Any], int]:
        """
        Handle POST request to send an SMS

        Expects a JSON body with:
        {
            "recipient_phone": {
                "country_code": "+1",
                "phone_number": "1234567890"
            },
            "message_body": "Your message here"
        }

        Returns:
            Tuple of (response dict, status code)
        """
        try:
            data = request.get_json()

            if not data:
                return {"error": "No JSON data provided"}, 400

            if "recipient_phone" not in data:
                return {"error": "recipient_phone is required"}, 400

            if "message_body" not in data:
                return {"error": "message_body is required"}, 400

            try:
                phone_data = data["recipient_phone"]
                recipient_phone = PhoneNumber(
                    country_code=phone_data.get("country_code", ""), phone_number=phone_data.get("phone_number", "")
                )
            except Exception as e:
                return {"error": f"Invalid phone number format: {str(e)}"}, 400

            params = SendSMSParams(recipient_phone=recipient_phone, message_body=data["message_body"])

            result = SMSNotificationService.send_sms(params=params)

            if result.success:
                response = {"success": True, "message": "SMS sent successfully", "message_sid": result.message_sid}
                if result.details:
                    response["details"] = result.details

                return response, 200
            else:
                return {"success": False, "error": result.error_message or "Failed to send SMS"}, 400

        except ValidationError as e:
            Logger.error(message=f"SMS validation error: {str(e)}")
            return {"error": str(e), "code": e.code}, 400

        except SMSNotificationError as e:
            Logger.error(message=f"SMS service error: {str(e)}")
            return {"error": str(e), "code": e.code}, 500

        except Exception as e:
            Logger.error(message=f"Unexpected error in SMS notification view: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500
