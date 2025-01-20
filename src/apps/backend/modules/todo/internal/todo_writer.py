from dataclasses import asdict

from bson.objectid import ObjectId
from pymongo import ReturnDocument

from modules.todo.errors import TodoNotFoundError
from modules.todo.internal.store.todo_model import TodoModel
from modules.todo.internal.store.todo_repository import TodoRepository
from modules.todo.internal.todo_util import TodoUtil
from modules.todo.types import CreateTodoParams, Todo


class TodoWriter:
    @staticmethod
    def create_todo(*, params: CreateTodoParams) -> Todo:
        # noinspection PyTypeChecker
        params_dict = asdict(params)
        todo_bson = TodoModel(**params_dict).to_bson()
        query = TodoRepository.collection().insert_one(todo_bson)
        todo = TodoRepository.collection().find_one({"_id": query.inserted_id})

        return TodoUtil.convert_todo_model_to_todo(TodoModel(**todo))

    @staticmethod
    def update_todo(**params) -> Todo:
        todo_id = params.pop("todo_id")
        updated_todo = TodoRepository.collection().find_one_and_update(
            {"_id": ObjectId(todo_id)}, {"$set": params}, return_document=ReturnDocument.AFTER
        )
        if updated_todo is None:
            raise TodoNotFoundError(f"Todo not found: {todo_id}")

        return TodoUtil.convert_todo_model_to_todo(TodoModel(**updated_todo))

    @staticmethod
    def delete_todo(todo_id: str) -> None:
        todo = TodoRepository.collection().find_one_and_delete({"_id": ObjectId(todo_id)})
        if todo is None:
            raise TodoNotFoundError(f"Todo not found: {todo_id}")
