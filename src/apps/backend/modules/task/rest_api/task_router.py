from flask import Blueprint

from modules.task.rest_api.task_view import TaskView


class TaskRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule("/tasks", view_func=TaskView.as_view("task_view"), methods=["POST", "GET"])
        return blueprint
