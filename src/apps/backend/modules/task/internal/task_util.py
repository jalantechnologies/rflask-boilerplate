from typing import Any

from modules.task.internal.store.task_model import TaskModel


class TaskUtil:
    @staticmethod
    def convert_task_bson_to_task(task_bson: dict[str, Any]) -> TaskModel:
        """
        Converts a BSON document from MongoDB into a TaskModel instance.
        """
        validated_task_data = TaskModel.from_bson(task_bson)
        return TaskModel(
            id=str(validated_task_data.id),
            title=validated_task_data.title,
            description=validated_task_data.description,
            status=validated_task_data.status,
            created_at=validated_task_data.created_at,
            updated_at=validated_task_data.updated_at,
        )
