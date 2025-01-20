from modules.todo.internal.todo_reader import TodoReader
from modules.todo.internal.todo_writer import TodoWriter
from modules.todo.types import CreateTodoParams, Todo, TodoSearchByIdParams, TodosSearchByUsernameParams


class TodoService:
    @staticmethod
    def get_todos_by_username(*, params: TodosSearchByUsernameParams) -> list[Todo]:
        return TodoReader.get_todos_by_username(params=params)

    @staticmethod
    def get_todo_by_id(*, params: TodoSearchByIdParams) -> Todo:
        return TodoReader.get_todo_by_id(params=params)

    @staticmethod
    def create_todo(*, params: CreateTodoParams) -> Todo:
        return TodoWriter.create_todo(params=params)

    @staticmethod
    def update_todo(**params) -> Todo:
        return TodoWriter.update_todo(**params)

    @staticmethod
    def delete_todo(todo_id: str) -> None:
        TodoWriter.delete_todo(todo_id=todo_id)
