# modules/todo/internal/todo_writer.py

from dataclasses import asdict
from datetime import datetime

from bson import ObjectId
from pymongo import ReturnDocument

from modules.todo.internal.store.todo_model import TodoModel
from modules.todo.internal.store.todo_repository import TodoRepository
from modules.todo.types import CreateTodoParams, Todo, UpdateTodoParams


class TodoWriter:
    @staticmethod
    def create_todo(account_id: str, params: CreateTodoParams) -> Todo:
        if isinstance(params.due_date, str):
            try:
                params.due_date = datetime.fromisoformat(params.due_date)
            except ValueError:
                params.due_date = None

        todo_bson = TodoModel(
            id=None,
            title=params.title,
            description=params.description,
            status=params.status,
            due_date=params.due_date,
            account_id=account_id,
        ).to_bson()

        result = TodoRepository.collection().insert_one(todo_bson)
        return Todo(
            id=str(result.inserted_id),
            title=params.title,
            description=params.description,
            status=params.status,
            due_date=params.due_date,
        )

    @staticmethod
    def update_todo(todo_id: str, params: UpdateTodoParams) -> Todo:
        update_data = {k: v for k, v in asdict(params).items() if v is not None}
        updated = TodoRepository.collection().find_one_and_update(
            {"_id": ObjectId(todo_id)}, {"$set": update_data}, return_document=ReturnDocument.AFTER
        )
        if updated:
            model = TodoModel.from_bson(updated)
            return Todo(
                id=str(model.id),
                title=model.title,
                description=model.description,
                status=model.status,
                due_date=model.due_date,
            )
        raise Exception("Todo not found")

    @staticmethod
    def delete_todo(todo_id: str):
        TodoRepository.collection().delete_one({"_id": ObjectId(todo_id)})
