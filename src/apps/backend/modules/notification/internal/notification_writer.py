from modules.notification.internal.notification_util import NotificationUtil
from modules.notification.internal.store.notification_model import NotificationModel
from modules.notification.internal.store.notification_repository import NotificationRepository
from modules.notification.types import CreateNotificationParams, Notification


class NotificationWriter:

    @staticmethod
    def create_notification(params: CreateNotificationParams) -> Notification:
        model = NotificationModel(
            user_id=params.user_id,
            payload=params.payload,
            type=params.type,
            channels=params.channels,
            schedule_at=params.schedule_at,
        )

        query = NotificationRepository.collection().insert_one(model.to_bson())
        notification_bson = NotificationRepository.collection().find_one({"_id": query.inserted_id})

        return NotificationUtil.convert_bson_to_notification(notification_bson)
