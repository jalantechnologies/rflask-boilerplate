from modules.logger.logger import Logger
from pymongo.collection import Collection
from pymongo.errors import OperationFailure
from modules.account.internal.store.account_model import AccountModel
from modules.application.repository import ApplicationRepository

ACCOUNT_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username"],
        "properties": {
            "active": {"bsonType": "bool"},
            "first_name": {"bsonType": "string"},
            "hashed_password": {"bsonType": "string", "description": "must be a string"},
            "last_name": {"bsonType": "string"},
            "phone_number": {
                "bsonType": ["object", "null"],
                "properties": {"country_code": {"bsonType": "string"}, "phone_number": {"bsonType": "string"}},
                "description": "must be an object with country_code and phone_number",
            },
            "username": {"bsonType": "string", "description": "must be a string and is required"},
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"},
        },
    }
}


class AccountRepository(ApplicationRepository):
    collection_name = AccountModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("username")

        add_validation_command = {
            "collMod": cls.collection_name,
            "validator": ACCOUNT_VALIDATION_SCHEMA,
            "validationLevel": "strict",
        }

        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            if "Collection does not exist" in str(e):
                collection.database.create_collection(cls.collection_name, validator=ACCOUNT_VALIDATION_SCHEMA)
            else:
                Logger.error(message=f"OperationFailure occurred for collection accounts: {e.details}")
        return True
