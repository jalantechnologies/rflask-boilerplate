from datetime import datetime

from bson import ObjectId

from modules.task.internal.store.task_model import TaskModel


class TaskUtil:
    @staticmethod
    def convert_task_bson_to_task(task_bson: dict) -> TaskModel:
        """
        Converts a BSON document from MongoDB into a TaskModel instance.
        """
        validated_task_data = TaskModel.from_bson(task_bson)
        return TaskModel(
            id=validated_task_data.id,
            title=validated_task_data.title,
            description=validated_task_data.description,
            created_at=validated_task_data.created_at,
            updated_at=validated_task_data.updated_at,
        )

    @staticmethod
    def serialize(obj):
        """Convert ObjectId to string and datetime to ISO format."""
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return obj
