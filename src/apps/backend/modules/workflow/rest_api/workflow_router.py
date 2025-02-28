from flask import Blueprint

from modules.workflow.rest_api.workflow_view import WorkflowView


class WorkflowRouter:
    WORKFLOWS_ROUTE: str = "/workflows"
    WORKFLOWS_ROUTE_BY_ID: str = "/workflows/<id>"

    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule(
            WorkflowRouter.WORKFLOWS_ROUTE,
            view_func=WorkflowView.as_view("workflow_list"),
            methods=["GET"],
        )
        blueprint.add_url_rule(
            WorkflowRouter.WORKFLOWS_ROUTE,
            view_func=WorkflowView.as_view("workflow_execute"),
            methods=["POST"],
        )
        blueprint.add_url_rule(
            WorkflowRouter.WORKFLOWS_ROUTE_BY_ID,
            view_func=WorkflowView.as_view("workflow_status"),
            methods=["GET"],
        )
        blueprint.add_url_rule(
            WorkflowRouter.WORKFLOWS_ROUTE_BY_ID,
            view_func=WorkflowView.as_view("workflow_cancel"),
            methods=["PATCH"],
        )
        blueprint.add_url_rule(
            WorkflowRouter.WORKFLOWS_ROUTE_BY_ID,
            view_func=WorkflowView.as_view("workflow_terminate"),
            methods=["DELETE"],
        )

        return blueprint
