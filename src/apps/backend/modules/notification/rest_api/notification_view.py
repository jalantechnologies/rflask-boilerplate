from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware
from modules.notification.notification_service import NotificationService
from modules.notification.types import FCMNotificationData, SendFCMParams


class NotificationView(MethodView):
    @access_auth_middleware
    def post(self) -> ResponseReturnValue:
        request_data = request.get_json()

        # Only allow authorized users (typically admins) to send to arbitrary users
        # Implement your own authorization logic here

        # Extract notification data
        notification_data = FCMNotificationData(
            title=request_data.get("title"),
            body=request_data.get("body"),
            data=request_data.get("data", {}),
            image_url=request_data.get("image_url"),
        )

        # Create params for sending notification
        params = SendFCMParams(
            notification=notification_data,
            user_ids=request_data.get("user_ids"),
            tokens=request_data.get("tokens"),
            topic=request_data.get("topic"),
        )

        # Send the notification
        result = NotificationService.send_push_notification(params=params)

        return jsonify({"message": "Notification sent", "results": result}), 200
