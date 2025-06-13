from typing import Any, Dict

from modules.logger.logger import Logger
from modules.notification.internal.firebase_notification_provider import FirebaseNotificationProvider
from modules.notification.types import SendNotificationParams


class NotificationService:
    _initialized = False

    @staticmethod
    def send_notification(*, params: SendNotificationParams) -> Dict[str, Any]:
        """
        Send a notification to a specific recipient

        Args:
            params: SendNotificationParams containing recipient and notification content

        Returns:
            dict: Response with success status and message ID or error
        """
        try:
            # Send notification via Firebase
            return FirebaseNotificationProvider.send_notification(params)
        except Exception as e:
            Logger.error(message=f"Error in notification service: {str(e)}")
            return {"success": False, "error": "Notification service error", "message": str(e)}

    @staticmethod
    def initialize() -> bool:
        """
        Initialize the notification service

        Returns:
            bool: True if initialization was successful
        """
        try:
            FirebaseNotificationProvider.initialize()
            NotificationService._initialized = True
            return True
        except Exception as e:
            Logger.error(message=f"Failed to initialize notification service: {str(e)}")
            return False
