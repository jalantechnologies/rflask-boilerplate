from modules.todo.internal.store.todo_model import TodoModel
from modules.todo.types import Todo


class TodoUtil:
    @staticmethod
    def convert_todo_model_to_todo(todo_model: TodoModel) -> Todo:
        return Todo(
            id=str(todo_model.id),
            username=todo_model.username,
            title=todo_model.title,
            description=todo_model.description,
            t_type=todo_model.t_type,
            completed=bool(todo_model.completed),
            due_date=todo_model.due_date,
        )
