# modules/todo/rest_api/todo_view.py

from flask import jsonify, request
from flask.views import MethodView

from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware
from modules.todo.internal.todo_reader import TodoReader
from modules.todo.internal.todo_writer import TodoWriter
from modules.todo.types import CreateTodoParams, UpdateTodoParams


class TodoView(MethodView):
    @access_auth_middleware
    def get(self):
        account_id = request.account_id
        todos = TodoReader.get_todos_for_user(account_id)
        return jsonify([todo.__dict__ for todo in todos]), 200

    @access_auth_middleware
    def post(self):
        account_id = request.account_id
        data = request.get_json()
        todo = TodoWriter.create_todo(account_id, CreateTodoParams(**data))
        return jsonify(todo.__dict__), 201

    @access_auth_middleware
    def patch(self, id: str):
        data = request.get_json()
        todo = TodoWriter.update_todo(id, UpdateTodoParams(**data))
        return jsonify(todo.__dict__), 200

    @access_auth_middleware
    def delete(self, id: str):
        TodoWriter.delete_todo(id)
        return "", 204
