from pymongo.collection import Collection

from modules.application.repository import ApplicationRepository
from modules.notification.internal.store.notification_model import NotificationModel

NOTIFICATION_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "payload", "type", "channels", "created_at", "updated_at"],
        "properties": {
            "user_id": {"bsonType": "string"},
            "payload": {"bsonType": "object"},
            "type": {"bsonType": "string"},
            "channels": {"bsonType": "array"},
            "schedule_at": {"bsonType": ["string", "null"]},
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"},
        },
    }
}


class NotificationRepository(ApplicationRepository):
    collection_name = NotificationModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("user_id")
        collection.create_index("schedule_at")
        collection.database.command(
            {"collMod": cls.collection_name, "validator": NOTIFICATION_VALIDATION_SCHEMA, "validationLevel": "strict"}
        )
        return True
