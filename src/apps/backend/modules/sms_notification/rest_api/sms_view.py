from typing import Any, Dict, Tuple

from flask import request
from flask.views import MethodView

from modules.account.account_service import AccountService
from modules.account.types import AccountSearchByIdParams, PhoneNumber
from modules.authentication.authentication_service import AuthenticationService
from modules.authentication.errors import AuthorizationHeaderNotFoundError, InvalidAuthorizationHeaderError
from modules.logger.logger import Logger
from modules.sms_notification.errors import SMSNotificationError, ValidationError
from modules.sms_notification.sms_service import SMSNotificationService
from modules.sms_notification.types import SendSMSParams


class SMSNotificationView(MethodView):
    """View for handling SMS notification API requests"""

    def _check_sms_notification_preference(self, account_id: str) -> bool:
        """
        Check if the user has enabled SMS notifications

        Args:
            account_id: The ID of the account to check

        Returns:
            True if SMS notifications are enabled, False otherwise
        """
        try:
            account_params = AccountSearchByIdParams(id=account_id)
            account = AccountService.get_account_by_id(params=account_params)

            if account.notification_preferences is None:
                return True

            return account.notification_preferences.sms
        except Exception as e:
            Logger.error(message=f"Error checking SMS notification preferences: {str(e)}")
            return True

    def _get_account_id_from_token(self) -> str:
        """
        Extract account_id from the authorization token

        Returns:
            The account ID from the token

        Raises:
            AuthorizationHeaderNotFoundError: If the Authorization header is missing
            InvalidAuthorizationHeaderError: If the Authorization header format is invalid
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise AuthorizationHeaderNotFoundError("Authorization header is missing.")

        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0] != "Bearer" or not parts[1]:
            raise InvalidAuthorizationHeaderError("Invalid authorization header.")

        auth_token = parts[1]
        auth_payload = AuthenticationService.verify_access_token(token=auth_token)
        return auth_payload.account_id

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
                account_id = self._get_account_id_from_token()
                sms_enabled = self._check_sms_notification_preference(account_id)

                if not sms_enabled:
                    return (
                        {
                            "success": False,
                            "error": "SMS notifications are disabled for this user",
                            "message": "The user has disabled SMS notifications in their preferences",
                        },
                        403,
                    )
            except (AuthorizationHeaderNotFoundError, InvalidAuthorizationHeaderError) as e:
                Logger.warning(message=f"Proceeding without checking SMS notification preferences: {str(e)}")

            try:
                phone_data = data["recipient_phone"]
                recipient_phone = PhoneNumber(
                    country_code=phone_data.get("country_code", ""), phone_number=phone_data.get("phone_number", "")
                )
            except Exception as e:
                return {"error": f"Invalid phone number format: {str(e)}"}, 400

            params = SendSMSParams(recipient_phone=recipient_phone, message_body=data["message_body"])

            Logger.info(
                message=f"Sending SMS to {recipient_phone.country_code} {recipient_phone.phone_number[:3]}*** (message preview: {data['message_body'][:50]}...)"
            )

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
