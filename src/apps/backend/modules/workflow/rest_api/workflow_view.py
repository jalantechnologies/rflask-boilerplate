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
            "arguments": [...]
        }
        """

        request_data = request.get_json()

        name = request_data.get("name")
        arguments = request_data.get("arguments", [])
        priority = request_data.get("priority", "DEFAULT")
        cron_schedule = request_data.get("cron_schedule", "")

        res = WorkflowService.queue_workflow(
            params=QueueWorkflowParams(
                name=name,
                arguments=arguments,
                priority=priority,
                cron_schedule=cron_schedule,
            )
        )

        return jsonify({"workflow_id": res}), 201

    def get(self, id: Optional[str] = None) -> ResponseReturnValue:
        if id:
            workflow_params = SearchWorkflowByIdParams(id=id)
            workflow_status = WorkflowService.get_workflow_status(
                params=workflow_params
            )

            return jsonify(workflow_status), 200

        else:
            workflows = WorkflowService.get_all_workflows()
            return jsonify({"workflows": workflows}), 200
