# modules/todo/internal/store/todo_repository.py

from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from modules.application.repository import ApplicationRepository
from modules.logger.logger import Logger
from modules.todo.internal.store.todo_model import TodoModel

TODO_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "status", "account_id", "created_at", "updated_at"],
        "properties": {
            "title": {"bsonType": "string"},
            "description": {"bsonType": ["string", "null"]},
            "status": {"bsonType": "string"},
            "due_date": {"bsonType": ["date", "null"]},
            "account_id": {"bsonType": "string"},
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"},
        },
    }
}


class TodoRepository(ApplicationRepository):
    collection_name = TodoModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("account_id")

        command = {"collMod": cls.collection_name, "validator": TODO_VALIDATION_SCHEMA, "validationLevel": "strict"}

        try:
            collection.database.command(command)
        except OperationFailure as e:
            if e.code == 26:
                collection.database.create_collection(cls.collection_name, validator=TODO_VALIDATION_SCHEMA)
            else:
                Logger.error(message=f"OperationFailure for todos: {e.details}")
        return True
