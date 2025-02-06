from modules.task.internal.store.task_model import TaskModel
from modules.task.types import Task


class TaskUtil:
    @staticmethod
    def convert_task_model_to_task(task_model: TaskModel) -> Task:
        return Task(
            id=str(task_model.id),
            account_id=str(task_model.account),
            title=task_model.title,
            description=task_model.description,
        )
