from modules.notification.internal.notification_reader import NotificationReader
from modules.notification.internal.notification_writer import NotificationWriter
from modules.notification.types import CreateNotificationParams, Notification


class NotificationService:

    @staticmethod
    def create_notification(*, params: CreateNotificationParams) -> Notification:
        return NotificationWriter.create_notification(params=params)

    @staticmethod
    def get_notification_by_id(*, notification_id: str) -> Notification:
        return NotificationReader.get_notification_by_id(notification_id=notification_id)
