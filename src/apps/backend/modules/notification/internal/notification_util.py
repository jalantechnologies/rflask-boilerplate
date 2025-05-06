from typing import Any

from modules.notification.types import Notification


class NotificationUtil:

    @staticmethod
    def convert_bson_to_notification(notification_bson: dict[str, Any]) -> Notification:
        return Notification(
            id=str(notification_bson["_id"]),
            user_id=notification_bson["user_id"],
            payload=notification_bson["payload"],
            type=notification_bson["type"],
            channels=notification_bson["channels"],
            schedule_at=notification_bson.get("schedule_at"),
            created_at=str(notification_bson["created_at"]),
        )
