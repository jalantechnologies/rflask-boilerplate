from dataclasses import asdict
from typing import List, Optional

from bson.objectid import ObjectId

from modules.task.errors import TaskWithIdNotFoundError
from modules.task.internal.store.task_repository import TaskRepository
from modules.task.internal.task_util import TaskUtil
from modules.task.types import Task, TaskSearchByIdParams, TaskSearchParams


class TaskReader:
    @staticmethod
    def get_task_by_id(*, params: TaskSearchByIdParams) -> Task:
        task_bson = TaskRepository.collection().find_one({"_id": ObjectId(params.id)})
        if task_bson is None:
            raise TaskWithIdNotFoundError(id=params.id)

        return TaskUtil.convert_task_bson_to_task(task_bson)

    @staticmethod
    def get_tasks(*, params: Optional[TaskSearchParams] = None) -> List[Task]:
        filters = asdict(params) if params else {}
        task_bson_list = TaskRepository.collection().find(filters)

        return [TaskUtil.convert_task_bson_to_task(task) for task in task_bson_list]
