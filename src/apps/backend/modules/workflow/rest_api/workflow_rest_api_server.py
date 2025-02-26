from flask import Blueprint

from modules.workflow.rest_api.workflow_router import WorkflowRouter


class WorkflowRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        workflow_api_blueprint = Blueprint("workflow", __name__)
        return WorkflowRouter.create_route(blueprint=workflow_api_blueprint)
