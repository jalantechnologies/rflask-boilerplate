from modules.todo.internal.store.todo_model import TodoModel
from modules.todo.types import Todo


class TodoUtil:
    @staticmethod
    def convert_todo_model_to_todo(todo_model: TodoModel) -> Todo:
        return Todo(
            id=str(todo_model.id),
            accountId=todo_model.account_id,
            title=todo_model.title,
            description=todo_model.description,
            type=todo_model.t_type,
            dueDate=todo_model.due_date,
            completed=bool(todo_model.completed),
            completedDate=todo_model.completed_date,
        )
