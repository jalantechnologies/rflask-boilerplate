from bson import ObjectId

from modules.notification.errors import NotificationNotFoundError
from modules.notification.internal.notification_util import NotificationUtil
from modules.notification.internal.store.notification_repository import NotificationRepository
from modules.notification.types import Notification


class NotificationReader:

    @staticmethod
    def get_notification_by_id(notification_id: str) -> Notification:
        notification_bson = NotificationRepository.collection().find_one({"_id": ObjectId(notification_id)})
        if notification_bson is None:
            raise NotificationNotFoundError(notification_id=notification_id)

        return NotificationUtil.convert_bson_to_notification(notification_bson)
