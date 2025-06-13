from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.logger.logger import Logger
from modules.notification.notification_service import NotificationService
from modules.notification.types import NotificationContent, NotificationRecipient, SendNotificationParams


class NotificationView(MethodView):
    """View controller for notification-related HTTP endpoints"""

    def post(self) -> ResponseReturnValue:
        """
        Endpoint to send a notification to a single device

        Accepts a JSON payload and transforms it into the appropriate
        domain objects before delegating to the notification service.

        Expected JSON payload:
        {
            "fcm_token": "string",
            "title": "string",
            "body": "string",
            "data": {"key": "value"} // optional
        }

        Returns:
            JSON response with success status or error details
        """
        try:
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400

            request_data = request.get_json()

            required_fields = ["fcm_token", "title", "body"]
            missing_fields = [field for field in required_fields if field not in request_data]

            if missing_fields:
                return jsonify({"error": "Missing required fields", "missing_fields": missing_fields}), 400

            fcm_token = request_data["fcm_token"]
            title = request_data["title"]
            body = request_data["body"]
            custom_data = request_data.get("data", {})

            recipient = NotificationRecipient(fcm_token=fcm_token)
            content = NotificationContent(title=title, body=body, data=custom_data)
            params = SendNotificationParams(recipient=recipient, content=content)

            Logger.info(message=f"Sending notification to token: {fcm_token[:15]}... (title: {title})")

            result = NotificationService.send_notification(params=params)

            if result.get("success", False):
                return jsonify(result), 200
            else:
                return jsonify(result), 400

        except Exception as e:
            Logger.error(message=f"Error in notification endpoint: {str(e)}")
            return jsonify({"success": False, "error": "Internal server error", "message": str(e)}), 500
