from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from modules.application.repository import ApplicationRepository
from modules.logger.logger import Logger
from modules.notification.internals.store.device_token_model import DeviceTokenModel

DEVICE_TOKEN_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["token", "user_id", "device_type", "last_active"],
        "properties": {
            "token": {"bsonType": "string", "description": "must be a string and is required"},
            "user_id": {"bsonType": "string", "description": "must be a string and is required"},
            "device_type": {"bsonType": "string", "description": "must be a string and is required"},
            "app_version": {"bsonType": "string", "description": "must be a string if present"},
            "last_active": {"bsonType": "date", "description": "must be a date and is required"},
            "created_at": {"bsonType": "date", "description": "must be a date"},
            "updated_at": {"bsonType": "date", "description": "must be a date"},
        },
    }
}


class DeviceTokenRepository(ApplicationRepository):
    collection_name = DeviceTokenModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("token", unique=True)
        collection.create_index("user_id")
        collection.create_index("last_active")

        add_validation_command = {
            "collMod": cls.collection_name,
            "validator": DEVICE_TOKEN_VALIDATION_SCHEMA,
            "validationLevel": "strict",
        }

        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            if e.code == 26:
                collection.database.create_collection(cls.collection_name, validator=DEVICE_TOKEN_VALIDATION_SCHEMA)
            else:
                Logger.error(message=f"OperationFailure occurred for collection device_tokens: {e.details}")
        return True
