from typing import List

from modules.task.errors import TaskCreationError, TaskNotFoundError, TaskServiceError
from modules.task.internal.task_reader import TaskReader
from modules.task.internal.task_writer import TaskWriter
from modules.task.types import CreateTaskParams, Task


class TaskService:
    @staticmethod
    def create_task(*, params: CreateTaskParams) -> Task:
        try:
            task = TaskWriter.create_task(params=params)
            return task

        except TaskCreationError as e:
            raise e

        except Exception as e:
            raise TaskCreationError(f"An unexpected error occurred while creating the task: {str(e)}")

    @staticmethod
    def get_tasks() -> List[Task]:
        try:
            task_list = TaskReader.get_tasks()
            if not task_list:
                raise TaskNotFoundError("No tasks were found in the service layer.")
            return task_list

        except TaskNotFoundError as e:
            raise e

        except Exception as e:
            raise TaskServiceError(f"Error occurred in TaskService: {str(e)}")
