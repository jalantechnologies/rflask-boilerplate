from modules.task.errors import TaskCreationError
from modules.task.internal.store.task_model import TaskModel
from modules.task.internal.store.task_repository import TaskRepository
from modules.task.types import CreateTaskParams, Task


class TaskWriter:
    @staticmethod
    def create_task(*, params: CreateTaskParams) -> Task:
        try:
            task_bson = TaskModel(id=None, title=params.title, description=params.description).to_bson()
            query = TaskRepository.collection().insert_one(task_bson)

            task_bson = TaskRepository.collection().find_one({"_id": query.inserted_id})

            return TaskModel.from_bson(task_bson)

        except Exception as e:
            raise TaskCreationError(f"An error occurred while creating the task: {str(e)}")
