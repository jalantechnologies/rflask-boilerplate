# src/apps/backend/modules/notification/rest_api/fcm_view.py
import logging
from typing import Any, Dict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.notification.fcm_service import FCMService
from modules.notification.types import FCMAndroidConfig, FCMApnsConfig, FCMErrorCode, FCMNotification, FCMWebpushConfig

logger = logging.getLogger(__name__)


class FCMView(MethodView):
    def post(self) -> ResponseReturnValue:
        """
        Send FCM notifications via multiple methods:

        1. Send to single token:
        {
            "type": "token",
            "token": "device_token_here",
            "notification": {
                "title": "Test Notification",
                "body": "This is a test message",
                "image": "https://example.com/image.png"
            },
            "data": {
                "key1": "value1",
                "key2": "value2"
            },
            "android_config": {
                "priority": "high",
                "ttl": "3600s",
                "collapse_key": "update"
            }
        }

        2. Send to multiple tokens:
        {
            "type": "tokens",
            "tokens": ["token1", "token2", "token3"],
            "notification": {
                "title": "Broadcast Message",
                "body": "This message goes to multiple devices"
            },
            "data": {
                "action": "update",
                "version": "1.2.0"
            }
        }

        3. Send to all users (via topic):
        {
            "type": "all",
            "topic": "all_users",  // optional, defaults to "all"
            "notification": {
                "title": "App Update",
                "body": "A new version of the app is available"
            },
            "data": {
                "update_required": "true"
            }
        }

        4. Simple notification (auto-detect single vs multiple):
        {
            "type": "simple",
            "tokens": ["token1"] or "single_token",
            "title": "Simple Message",
            "body": "This is a simple notification",
            "data": {
                "simple": "true"
            },
            "android_priority": "high"
        }
        """

        try:
            request_data = request.get_json()

            if not request_data:
                return jsonify({"error": "Request body is required", "success": False}), 400

            fcm_type = request_data.get("type", "simple")

            if fcm_type == "token":
                response = self._handle_single_token(request_data)
            elif fcm_type == "tokens":
                response = self._handle_multiple_tokens(request_data)
            elif fcm_type == "all":
                response = self._handle_send_to_all(request_data)
            elif fcm_type == "simple":
                response = self._handle_simple_fcm(request_data)
            else:
                return (
                    jsonify(
                        {
                            "error": f"Invalid FCM type: {fcm_type}. Supported types: token, tokens, all, simple",
                            "success": False,
                            "code": FCMErrorCode.VALIDATION_ERROR,
                        }
                    ),
                    400,
                )

            response_data = {
                "success": response.success,
                "sent_count": response.sent_count,
                "failed_count": response.failed_count,
                "message_ids": response.message_ids,
                "errors": response.errors,
            }

            # Include failure details if available
            if response.failure_details:
                response_data["failure_details"] = response.failure_details

            status_code = 200 if response.success else 400
            return jsonify(response_data), status_code

        except ValueError as e:
            logger.error(f"Validation error in FCM API: {e}")
            return jsonify({"success": False, "message": str(e), "code": FCMErrorCode.VALIDATION_ERROR}), 400
        except Exception as e:
            logger.exception(f"Unexpected error in FCM API: {e}")
            return (
                jsonify({"success": False, "message": "Internal server error", "code": FCMErrorCode.SERVICE_ERROR}),
                500,
            )

    def _handle_single_token(self, data: Dict[str, Any]) -> Any:
        """Handle sending FCM to a single token"""
        try:
            token = data.get("token")
            if not token:
                raise ValueError("Token is required")

            notification = self._parse_notification(data.get("notification"))
            data_payload = data.get("data")
            android_config = self._parse_android_config(data.get("android_config"))
            apns_config = self._parse_apns_config(data.get("apns_config"))
            webpush_config = self._parse_webpush_config(data.get("webpush_config"))

            return FCMService.send_fcm_to_token(
                token=token,
                notification=notification,
                data=data_payload,
                android_config=android_config,
                apns_config=apns_config,
                webpush_config=webpush_config,
            )

        except Exception as e:
            logger.exception(f"Error in _handle_single_token: {e}")
            raise e

    def _handle_multiple_tokens(self, data: Dict[str, Any]) -> Any:
        """Handle sending FCM to multiple tokens"""
        try:
            tokens = data.get("tokens")
            if not tokens:
                raise ValueError("Tokens are required")

            if not isinstance(tokens, list):
                raise ValueError("Tokens must be a list")

            notification = self._parse_notification(data.get("notification"))
            data_payload = data.get("data")
            android_config = self._parse_android_config(data.get("android_config"))
            apns_config = self._parse_apns_config(data.get("apns_config"))
            webpush_config = self._parse_webpush_config(data.get("webpush_config"))

            return FCMService.send_fcm_to_tokens(
                tokens=tokens,
                notification=notification,
                data=data_payload,
                android_config=android_config,
                apns_config=apns_config,
                webpush_config=webpush_config,
            )

        except Exception as e:
            logger.exception(f"Error in _handle_multiple_tokens: {e}")
            raise e

    def _handle_send_to_all(self, data: Dict[str, Any]) -> Any:
        """Handle sending FCM to all users via topic"""
        try:
            topic = data.get("topic", "all")

            notification = self._parse_notification(data.get("notification"))
            data_payload = data.get("data")
            android_config = self._parse_android_config(data.get("android_config"))
            apns_config = self._parse_apns_config(data.get("apns_config"))
            webpush_config = self._parse_webpush_config(data.get("webpush_config"))

            return FCMService.send_fcm_to_all(
                topic=topic,
                notification=notification,
                data=data_payload,
                android_config=android_config,
                apns_config=apns_config,
                webpush_config=webpush_config,
            )

        except Exception as e:
            logger.exception(f"Error in _handle_send_to_all: {e}")
            raise e

    def _handle_simple_fcm(self, data: Dict[str, Any]) -> Any:
        """Handle simple FCM notification"""
        try:
            tokens = data.get("tokens")
            title = data.get("title")
            body = data.get("body")

            if not tokens:
                raise ValueError("Tokens are required")
            if not title:
                raise ValueError("Title is required")
            if not body:
                raise ValueError("Body is required")

            data_payload = data.get("data")
            image = data.get("image")
            android_priority = data.get("android_priority")

            return FCMService.send_simple_fcm(
                tokens=tokens, title=title, body=body, data=data_payload, image=image, android_priority=android_priority
            )

        except Exception as e:
            logger.exception(f"Error in _handle_simple_fcm: {e}")
            raise e

    def _parse_notification(self, notification_data: Dict[str, Any]) -> FCMNotification | None:
        """Parse notification data"""
        if not notification_data:
            return None

        title = notification_data.get("title")
        body = notification_data.get("body")

        if not title or not body:
            raise ValueError("Notification title and body are required")

        return FCMNotification(title=title, body=body, image=notification_data.get("image"))

    def _parse_android_config(self, android_data: Dict[str, Any]) -> FCMAndroidConfig | None:
        """Parse Android config data"""
        if not android_data:
            return None

        return FCMAndroidConfig(
            priority=android_data.get("priority"),
            ttl=android_data.get("ttl"),
            collapse_key=android_data.get("collapse_key"),
            data=android_data.get("data"),
            notification=android_data.get("notification"),
        )

    def _parse_apns_config(self, apns_data: Dict[str, Any]) -> FCMApnsConfig | None:
        """Parse APNS config data"""
        if not apns_data:
            return None

        return FCMApnsConfig(headers=apns_data.get("headers"), payload=apns_data.get("payload"))

    def _parse_webpush_config(self, webpush_data: Dict[str, Any]) -> FCMWebpushConfig | None:
        """Parse Webpush config data"""
        if not webpush_data:
            return None

        return FCMWebpushConfig(
            headers=webpush_data.get("headers"),
            data=webpush_data.get("data"),
            notification=webpush_data.get("notification"),
        )
