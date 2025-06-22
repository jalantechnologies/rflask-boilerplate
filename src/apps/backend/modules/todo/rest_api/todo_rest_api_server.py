# modules/todo/rest_api/todo_rest_api_server.py

from flask import Blueprint

from modules.todo.rest_api.todo_router import TodoRouter


class TodoRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        todo_api_blueprint = Blueprint("todo", __name__)
        return TodoRouter.create_route(blueprint=todo_api_blueprint)
