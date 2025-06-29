from typing import Optional

from modules.notification.internals.firebase_service import FirebaseService
from modules.notification.types import PushNotificationParams


class PushNotificationService:
    @staticmethod
    def send_push_notification(*, params: PushNotificationParams) -> Optional[str]:
        """
        Send a push notification using Firebase Cloud Messaging.

        Args:
            params: PushNotificationParams with notification details

        Returns:
            str: The message ID from FCM or None if sending failed
        """
        return FirebaseService.send_push_notification(params=params)
