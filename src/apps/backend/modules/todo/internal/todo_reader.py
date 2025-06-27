# modules/todo/internal/todo_reader.py

from typing import List

from modules.todo.internal.store.todo_model import TodoModel
from modules.todo.internal.store.todo_repository import TodoRepository
from modules.todo.types import Todo


class TodoReader:
    @staticmethod
    def get_todos_for_user(account_id: str) -> List[Todo]:
        todos = []
        for doc in TodoRepository.collection().find({"account_id": account_id}):
            model = TodoModel.from_bson(doc)
            todos.append(
                Todo(
                    id=str(model.id),
                    title=model.title,
                    description=model.description,
                    status=model.status,
                    due_date=model.due_date,
                )
            )
        return todos
