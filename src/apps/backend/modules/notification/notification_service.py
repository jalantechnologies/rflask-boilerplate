from typing import Any, Dict

from modules.logger.logger import Logger
from modules.notification.fcm_token_service import FCMTokenService
from modules.notification.internal.firebase_notification_provider import FirebaseNotificationProvider
from modules.notification.types import (
    MultipleNotificationRecipients,
    NotificationContent,
    SendMultipleNotificationsParams,
    SendNotificationParams,
)


class NotificationService:
    """
    Service responsible for sending notifications to end-users.
    Acts as a facade to abstract different notification providers implementation details.
    """

    _initialized = False

    @staticmethod
    def send_notification(*, params: SendNotificationParams) -> Dict[str, Any]:
        """
        Sends a notification to a specific recipient.

        This method abstracts the underlying notification provider (Firebase)
        to maintain a consistent interface if additional providers are added later.

        Args:
            params: Contains recipient information and notification content

        Returns:
            Response containing success status and message ID or error details
        """
        try:
            return FirebaseNotificationProvider.send_notification(params)
        except Exception as e:
            Logger.error(message=f"Error in notification service: {str(e)}")
            return {"success": False, "error": "Notification service error", "message": str(e)}

    @staticmethod
    def initialize() -> bool:
        """
        Initializes the notification service and its providers.

        Should be called during application startup to ensure the
        notification infrastructure is ready before handling requests.

        Returns:
            True if initialization was successful, False otherwise
        """
        try:
            FirebaseNotificationProvider.initialize()
            NotificationService._initialized = True
            return True
        except Exception as e:
            Logger.error(message=f"Failed to initialize notification service: {str(e)}")
            return False

    @classmethod
    def send_multiple_notifications(cls, params: SendMultipleNotificationsParams) -> Dict[str, Any]:
        """
        Send the same notification to multiple devices

        Args:
            params: Parameters for sending notifications to multiple recipients

        Returns:
            Dict containing success status and details of succeeded/failed tokens
        """
        return FirebaseNotificationProvider.send_multiple_notifications(params=params)

    @staticmethod
    def send_notification_to_all_devices(*, content: NotificationContent) -> Dict[str, Any]:
        """
        Send notification to all devices that have active FCM tokens.

        This method fetches all active FCM tokens from the database and sends
        the same notification to all of them.

        Args:
            content: The notification content (title, body, data)

        Returns:
            Response containing success status and details of succeeded/failed tokens
        """
        try:
            tokens_result = FCMTokenService.get_all_active_tokens()

            if not tokens_result.get("success", False):
                Logger.error(message="Failed to retrieve active FCM tokens")
                return {
                    "success": False,
                    "error": "Failed to retrieve active tokens",
                    "message": tokens_result.get("message", "Unknown error"),
                }

            fcm_tokens = tokens_result.get("tokens", [])

            if not fcm_tokens:
                Logger.info(message="No active FCM tokens found")
                return {
                    "success": True,
                    "message": "No active devices found to send notifications to",
                    "total_tokens": 0,
                    "successful_tokens": 0,
                    "failed_tokens": 0,
                }

            recipients = MultipleNotificationRecipients(fcm_tokens=fcm_tokens)
            params = SendMultipleNotificationsParams(recipients=recipients, content=content)

            result = NotificationService.send_multiple_notifications(params=params)

            result["operation"] = "send_to_all_devices"
            result["total_active_tokens_found"] = len(fcm_tokens)

            Logger.info(
                message=f"Sent notification to all devices: {result.get('successful_tokens', 0)}/{len(fcm_tokens)} successful"
            )

            return result

        except Exception as e:
            Logger.error(message=f"Error in send_notification_to_all_devices: {str(e)}")
            return {"success": False, "error": "Failed to send notification to all devices", "message": str(e)}
