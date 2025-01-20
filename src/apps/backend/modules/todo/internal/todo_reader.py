from typing import List

from bson import ObjectId

from modules.todo.errors import TodoNotFoundError
from modules.todo.internal.store.todo_model import TodoModel
from modules.todo.internal.store.todo_repository import TodoRepository
from modules.todo.internal.todo_util import TodoUtil
from modules.todo.types import Todo, TodoSearchByIdParams, TodosSearchByUsernameParams


class TodoReader:
    @staticmethod
    def get_todos_by_username(*, params: TodosSearchByUsernameParams) -> List[Todo]:
        todos = TodoRepository.collection().find({"username": params.username})
        if todos.count() == 0:
            raise TodoNotFoundError(f"Todos for username:: {params.username}, not found")

        return [TodoUtil.convert_todo_model_to_todo(TodoModel(**todo)) for todo in todos]

    @staticmethod
    def get_todo_by_id(*, params: TodoSearchByIdParams) -> Todo:
        todo = TodoRepository.collection().find_one({"_id": ObjectId(params.todo_id)})
        if todo is None:
            raise TodoNotFoundError(f"Todo with id:: {params.todo_id}, not found")

        return TodoUtil.convert_todo_model_to_todo(TodoModel(**todo))
