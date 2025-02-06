from modules.task.internal.store.task_repository import TaskRepository
from modules.task.internal.store.task_model import TaskModel
from modules.task.types import DeleteTaskParams, CreateTaskParams, UpdateTaskParams
from modules.task.internal.task_util import TaskUtil
from dataclasses import asdict
from bson.objectid import ObjectId
from pymongo import ReturnDocument


class TaskWriter:
    @staticmethod
    def create_task(*, params: CreateTaskParams):
        params_dict = asdict(params)
        task_bson = TaskModel(account=params.account_id, **params_dict).to_bson()
        query = TaskRepository.collection().insert_one(task_bson)
        task = TaskRepository.collection().find_one({"_id": query.inserted_id})
        return TaskUtil.convert_task_model_to_task(TaskModel(**task))

    @staticmethod
    def update_task(*, params: UpdateTaskParams):
        params_dict = asdict(params)
        task_bson = TaskModel(account=params.account_id, **params_dict).to_bson()
        query = TaskRepository.collection().find_one_and_update(
            {"_id": ObjectId(params.task_id)}, {"$set": task_bson}, return_document=ReturnDocument.AFTER
        )

        if not query:
            return None

        return TaskUtil.convert_task_model_to_task(TaskModel(**query))

    @staticmethod
    def delete_task(*, params: DeleteTaskParams) -> bool:
        delete_result = TaskRepository.collection().delete_one(
            {"_id": ObjectId(params.task_id), "account": params.account_id}
        )

        if delete_result.deleted_count == 0:
            return False

        return True
