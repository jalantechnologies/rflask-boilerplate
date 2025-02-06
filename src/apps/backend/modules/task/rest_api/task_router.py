from flask import Blueprint

from modules.task.rest_api.task_view import TaskView


class TaskRouter:

    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule("/tasks", view_func=TaskView.as_view("task_create"), methods=["POST"])
        blueprint.add_url_rule("/tasks", view_func=TaskView.as_view("task_view_for_account"), methods=["GET"])
        blueprint.add_url_rule(
            "/tasks/<task_id>", view_func=TaskView.as_view("task_update_for_account"), methods=["PATCH"]
        )
        blueprint.add_url_rule(
            "/tasks/<task_id>", view_func=TaskView.as_view("task_delete_for_account"), methods=["DELETE"]
        )
        return blueprint
