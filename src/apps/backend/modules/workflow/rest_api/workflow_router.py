from flask import Blueprint

from modules.workflow.rest_api.workflow_view import WorkflowView


class WorkflowRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule("/workflows", view_func=WorkflowView.as_view("workflow_list"), methods=["GET"])
        blueprint.add_url_rule("/workflows/<id>", view_func=WorkflowView.as_view("workflow_status"), methods=["GET"])
        blueprint.add_url_rule("/workflows", view_func=WorkflowView.as_view("workflow_execute"), methods=["POST"])
        return blueprint
