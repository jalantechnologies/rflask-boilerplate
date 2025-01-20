from dataclasses import asdict
from datetime import datetime
from typing import Optional

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.todo.todo_service import TodoService
from modules.todo.types import CreateTodoParams, TodoSearchByIdParams, TodosSearchByUsernameParams


class TodoView(MethodView):
    # @access_auth_middleware
    def post(self) -> ResponseReturnValue:
        request_data = request.get_json()
        request_data["due_date"] = datetime.fromisoformat(request_data["due_date"])
        todo_params: CreateTodoParams = CreateTodoParams(**request_data)
        todo = TodoService.create_todo(params=todo_params)
        todo_dict = asdict(todo)
        return jsonify(todo_dict), 201

    # @access_auth_middleware
    def get(self, todo_id: Optional[str] = None) -> ResponseReturnValue:
        if todo_id:
            todo_params = TodoSearchByIdParams(todo_id=todo_id)
            todo = TodoService.get_todo_by_id(params=todo_params)
            todo_dict = asdict(todo)
            return jsonify(todo_dict), 200
        username = request.args.get("username")
        todos_params = TodosSearchByUsernameParams(username=username)
        todos = TodoService.get_todos_by_username(params=todos_params)
        todos_list = [asdict(todo) for todo in todos]
        return jsonify(todos_list), 200

    # @access_auth_middleware
    def patch(self, todo_id: str) -> ResponseReturnValue:
        request_data = request.get_json()
        request_data["todo_id"] = todo_id
        todo = TodoService.update_todo(**request_data)
        todo_dict = asdict(todo)
        return jsonify(todo_dict), 200

    def delete(self, todo_id: str) -> ResponseReturnValue:
        TodoService.delete_todo(todo_id=todo_id)
        return jsonify({}), 204
