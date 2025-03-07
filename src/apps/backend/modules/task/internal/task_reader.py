from typing import List

from modules.task.errors import DatabaseError, TaskNotFoundError
from modules.task.internal.store.task_repository import TaskRepository
from modules.task.internal.task_util import TaskUtil
from modules.task.types import Task


class TaskReader:
    @staticmethod
    def get_tasks() -> List[Task]:
        try:
            task_bson_list = list(TaskRepository.collection().find())

            if not task_bson_list:
                raise TaskNotFoundError("No tasks found in the database.")

            return [TaskUtil.convert_task_bson_to_task(task) for task in task_bson_list]

        except Exception as e:
            raise DatabaseError(f"An error occurred while fetching tasks: {str(e)}")
