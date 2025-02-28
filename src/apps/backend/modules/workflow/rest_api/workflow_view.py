from typing import Optional

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.workflow.types import QueueWorkflowParams, SearchWorkflowByIdParams
from modules.workflow.workflow_service import WorkflowService


class WorkflowView(MethodView):
    def post(self) -> ResponseReturnValue:
        """
        Expected request body:

        {
            "name": "...",
            "arguments": [...] # Optional list of arguments
            "cron_schedule": "..." # Optional crontab expression
        }
        """

        request_data = request.get_json()

        name = request_data.get("name")
        arguments = request_data.get("arguments", [])
        cron_schedule = request_data.get("cron_schedule", "")

        res = WorkflowService.queue_workflow(
            params=QueueWorkflowParams(
                name=name,
                arguments=arguments,
                cron_schedule=cron_schedule,
            )
        )

        return jsonify({"workflow_id": res}), 201

    def get(self, id: Optional[str] = None) -> ResponseReturnValue:
        if id:
            workflow_params = SearchWorkflowByIdParams(id=id)
            workflow_status = WorkflowService.get_workflow_details(
                params=workflow_params
            )

            return jsonify(workflow_status), 200

        else:
            workflows = WorkflowService.get_all_workflows()
            return jsonify({"workflows": workflows}), 200

    def patch(self, id: str) -> ResponseReturnValue:
        WorkflowService.cancel_workflow(params=SearchWorkflowByIdParams(id=id))
        return jsonify({"message": f"Workflow {id} cancelled"}), 200

    def delete(self, id: str) -> ResponseReturnValue:
        WorkflowService.terminate_workflow(params=SearchWorkflowByIdParams(id=id))
        return jsonify({"message": f"Workflow {id} terminated"}), 200
