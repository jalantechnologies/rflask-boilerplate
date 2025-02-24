from modules.worker.errors import TaskIdNotFoundError, TaskNameNotFoundError
from modules.worker.types import QueueTaskParams, SearchTaskByIdParams, SearchTaskByNameParams
from tasks import celery


class WorkerService:
    @staticmethod
    def get_task_by_name(*, params: SearchTaskByNameParams) -> celery.Task:
        task = celery.tasks.get(params.name)

        if not task:
            raise TaskNameNotFoundError(task_name=params.name)

        return task

    @staticmethod
    def get_task_status(*, params: SearchTaskByIdParams) -> celery.AsyncResult:
        res = celery.AsyncResult(params.id)

        if res.state == "PENDING":
            raise TaskIdNotFoundError(task_id=params.id)

        return res

    @staticmethod
    def get_all_tasks() -> list[str]:
        all_tasks = celery.tasks.keys()
        custom_tasks = [t for t in all_tasks if not t.startswith("celery.")]
        return custom_tasks

    @staticmethod
    def queue_task(*, params: QueueTaskParams) -> celery.AsyncResult:
        res = params.task.delay(**params.task_params)
        return res
