from dataclasses import asdict

from bson.objectid import ObjectId
from pymongo import ReturnDocument

from modules.task.errors import TaskWithIdNotFoundError
from modules.task.internal.store.task_model import TaskModel
from modules.task.internal.store.task_repository import TaskRepository
from modules.task.types import CreateTaskParams, Task


class TaskWriter:
    @staticmethod
    def create_task(*, params: CreateTaskParams) -> Task:
        asdict(params)
        task_bson = TaskModel(id=None, title=params.title, description=params.description).to_bson()
        query = TaskRepository.collection().insert_one(task_bson)
        task_bson = TaskRepository.collection().find_one({"_id": query.inserted_id})

        return TaskModel.from_bson(task_bson)

    @staticmethod
    def update_task(task_id: str, params: CreateTaskParams) -> Task:
        updated_task = TaskRepository.collection().find_one_and_update(
            {"_id": ObjectId(task_id)}, {"$set": asdict(params)}, return_document=ReturnDocument.AFTER
        )
        if updated_task is None:
            raise TaskWithIdNotFoundError(id=task_id)

        return TaskModel.from_bson(updated_task)
