# modules/todo/rest_api/todo_router.py

from flask import Blueprint

from modules.todo.rest_api.todo_view import TodoView


class TodoRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule("/todos", view_func=TodoView.as_view("todo_view"))
        blueprint.add_url_rule("/todos/<id>", view_func=TodoView.as_view("todo_update"), methods=["PATCH"])
        blueprint.add_url_rule("/todos/<id>", view_func=TodoView.as_view("todo_delete"), methods=["DELETE"])
        return blueprint
