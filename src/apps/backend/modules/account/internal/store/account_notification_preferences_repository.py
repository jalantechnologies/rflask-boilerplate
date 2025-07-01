from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from modules.account.internal.store.account_notification_preferences_model import AccountNotificationPreferencesModel
from modules.application.repository import ApplicationRepository
from modules.logger.logger import Logger

ACCOUNT_NOTIFICATION_PREFERENCES_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["account_id", "email_enabled", "sms_enabled", "push_enabled", "created_at", "updated_at"],
        "properties": {
            "account_id": {"bsonType": "string", "description": "must be a string and is required"},
            "email_enabled": {"bsonType": "bool", "description": "must be a boolean and is required"},
            "push_enabled": {"bsonType": "bool", "description": "must be a boolean and is required"},
            "sms_enabled": {"bsonType": "bool", "description": "must be a boolean and is required"},
            "created_at": {"bsonType": "date", "description": "must be a valid date"},
            "updated_at": {"bsonType": "date", "description": "must be a valid date"},
        },
    }
}


class AccountNotificationPreferencesRepository(ApplicationRepository):
    collection_name = AccountNotificationPreferencesModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("account_id", unique=True)

        add_validation_command = {
            "collMod": cls.collection_name,
            "validator": ACCOUNT_NOTIFICATION_PREFERENCES_VALIDATION_SCHEMA,
            "validationLevel": "strict",
        }

        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            if e.code == 26:
                collection.database.create_collection(
                    cls.collection_name, validator=ACCOUNT_NOTIFICATION_PREFERENCES_VALIDATION_SCHEMA
                )
            else:
                Logger.error(
                    message=f"OperationFailure occurred for collection account_notification_preferences: {e.details}"
                )
        return True
