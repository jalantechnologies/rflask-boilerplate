from datetime import datetime, timezone

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from modules.application.repository import ApplicationRepository
from modules.comment.internal.store.comment_model import CommentModel
from modules.logger.logger import Logger

COMMENT_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["task_id", "user_id", "content", "created_at", "updated_at"],
        "properties": {
            "task_id": {"bsonType": "objectId", "description": "must be a valid ObjectId reference to a task"},
            "user_id": {"bsonType": "objectId", "description": "must be a valid ObjectId reference to a user"},
            "content": {"bsonType": "string", "description": "must be a string"},
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"},
        },
    }
}


class CommentRepository(ApplicationRepository):
    collection_name = "comments"

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("task_id")
        collection.create_index("user_id")
        collection.create_index("created_at")

        add_validation_command = {
            "collMod": cls.collection_name,
            "validator": COMMENT_VALIDATION_SCHEMA,
            "validationLevel": "strict",
        }

        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            if e.code == 26:
                collection.database.create_collection(cls.collection_name, validator=COMMENT_VALIDATION_SCHEMA)
            else:
                Logger.error(message=f"OperationFailure occurred for collection comments: {e.details}")
        return True

    @classmethod
    def create_comment(cls, collection: Collection, comment: CommentModel) -> str:
        comment_data = comment.to_bson()
        result = collection.insert_one(comment_data)
        return str(result.inserted_id)

    @classmethod
    def get_comments_by_task_id(cls, collection: Collection, task_id: str) -> list:
        comments = collection.find({"task_id": ObjectId(task_id)})
        return [CommentModel.from_bson(comment) for comment in comments]

    @classmethod
    def update_comment(cls, collection: Collection, comment_id: str, content: str) -> bool:
        result = collection.update_one(
            {"_id": ObjectId(comment_id)}, {"$set": {"content": content, "updated_at": datetime.now(timezone.utc)}}
        )
        return result.modified_count > 0
