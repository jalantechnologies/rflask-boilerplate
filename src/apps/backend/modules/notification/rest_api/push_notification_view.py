from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware
from modules.notification.notification_service import NotificationService
from modules.notification.types import PushNotificationParams


class PushNotificationView(MethodView):
    @access_auth_middleware
    def post(self) -> ResponseReturnValue:
        """
        Send a push notification.

        Request body example:
        {
            "title": "Notification Title",
            "message": "Notification message content",
            "device_type": "android", // optional, can be "android", "ios", or omitted for all
            "topic": "custom_topic", // optional, defaults to "all_users"
            "data": { // optional additional data
                "key1": "value1",
                "key2": "value2"
            },
            "image_url": "https://example.com/image.jpg", // optional
            "account_id": "12345" // optional, to check notification preferences
        }

        Returns:
            200 OK with the FCM response ID or notification status
        """
        request_data = request.get_json()

        # Extract parameters from request
        params = PushNotificationParams(
            title=request_data.get("title", ""),
            message=request_data.get("message", ""),
            device_type=request_data.get("device_type"),
            topic=request_data.get("topic", "all_users"),
            data=request_data.get("data"),
            image_url=request_data.get("image_url"),
        )

        # Check if account_id is provided
        account_id = request_data.get("account_id")

        # Send notification
        response = NotificationService.send_push_notification(params=params, account_id=account_id)

        if response:
            return jsonify({"success": True, "message": "Push notification sent successfully", "id": response}), 200
        else:
            return (
                jsonify(
                    {"success": True, "message": "Push notification processed (no delivery confirmation available)"}
                ),
                200,
            )
