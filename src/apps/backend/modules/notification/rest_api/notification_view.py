from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.logger.logger import Logger
from modules.notification.notification_service import NotificationService
from modules.notification.types import (
    MultipleNotificationRecipients,
    NotificationContent,
    NotificationRecipient,
    SendMultipleNotificationsParams,
    SendNotificationParams,
)


class NotificationView(MethodView):
    """View controller for notification-related HTTP endpoints"""

    methods = ["POST"]

    def dispatch_request(self, *args, **kwargs):
        """
        Override dispatch to handle different endpoints with the same view class

        This allows us to use endpoint name to route to the correct handler method
        """
        endpoint = request.endpoint

        if endpoint and endpoint.endswith("multiple_notification_view"):
            return self.handle_multiple_notifications()
        else:
            return self.handle_single_notification()

    def handle_single_notification(self) -> ResponseReturnValue:
        """
        Process a request to send a notification to a single device
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

    def handle_multiple_notifications(self) -> ResponseReturnValue:
        """
        Process a request to send a notification to multiple devices
        """
        try:
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400

            request_data = request.get_json()

            required_fields = ["fcm_tokens", "title", "body"]
            missing_fields = [field for field in required_fields if field not in request_data]

            if missing_fields:
                return jsonify({"error": "Missing required fields", "missing_fields": missing_fields}), 400

            fcm_tokens = request_data["fcm_tokens"]
            title = request_data["title"]
            body = request_data["body"]
            custom_data = request_data.get("data", {})

            if not isinstance(fcm_tokens, list):
                return jsonify({"error": "fcm_tokens must be a list of strings"}), 400

            if len(fcm_tokens) == 0:
                return jsonify({"error": "fcm_tokens list cannot be empty"}), 400

            recipients = MultipleNotificationRecipients(fcm_tokens=fcm_tokens)
            content = NotificationContent(title=title, body=body, data=custom_data)
            params = SendMultipleNotificationsParams(recipients=recipients, content=content)

            Logger.info(message=f"Sending notification to {len(fcm_tokens)} devices (title: {title})")

            result = NotificationService.send_multiple_notifications(params=params)

            if result.get("success", False):
                return jsonify(result), 200
            else:
                return jsonify(result), 400

        except Exception as e:
            Logger.error(message=f"Error in multiple notification endpoint: {str(e)}")
            return jsonify({"success": False, "error": "Internal server error", "message": str(e)}), 500

    def post(self) -> ResponseReturnValue:
        """
        Handle POST requests - dispatches to the appropriate handler
        based on the endpoint
        """
        endpoint = request.endpoint

        if endpoint and endpoint.endswith("multiple_notification_view"):
            return self.handle_multiple_notifications()
        else:
            return self.handle_single_notification()
