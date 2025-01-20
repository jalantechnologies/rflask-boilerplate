from flask import Blueprint

from modules.todo.rest_api.todo_view import TodoView


class TodoRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule("/todos", view_func=TodoView.as_view("todos_view_all_create"), methods=["POST", "GET"])
        blueprint.add_url_rule("/todos/<todo_id>", view_func=TodoView.as_view("todos_view_by_id"), methods=["GET"])
        blueprint.add_url_rule("/todos/<todo_id>", view_func=TodoView.as_view("todos_update"), methods=["PATCH"])
        blueprint.add_url_rule("/todos/<todo_id>", view_func=TodoView.as_view("todos_delete"), methods=["DELETE"])
        return blueprint
