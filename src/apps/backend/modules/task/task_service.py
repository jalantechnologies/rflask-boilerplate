from modules.task.internal.task_reader import TaskReader
from modules.task.internal.task_writer import TaskWriter
from modules.task.types import CreateTaskParams, Task, TaskSearchByIdParams, UpdateTaskParams


class TaskService:
    @staticmethod
    def create_task(*, params: CreateTaskParams) -> Task:
        return TaskWriter.create_task(params=params)

    @staticmethod
    def get_task_by_id(*, params: TaskSearchByIdParams) -> Task:
        return TaskReader.get_task_by_id(params=params)

    @staticmethod
    def update_task(*, params: UpdateTaskParams) -> Task:
        return TaskWriter.update_task(params=params)

    @staticmethod
    def delete_task(*, task_id: str) -> None:
        return TaskWriter.delete_task(task_id=task_id)
