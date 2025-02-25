from typing import Optional

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.worker.types import QueueWorkflowParams, SearchWorkflowByIdParams, SearchWorkflowByNameParams
from modules.worker.worker_service import WorkerService


class WorkerView(MethodView):
    def post(self) -> ResponseReturnValue:
        """
        Expected request body:

        {
            "workflow_name": "...",
            "workflow_params": [...]
        }
        """

        request_data = request.get_json()

        workflow_name = request_data.get("workflow_name")
        workflow_params = request_data.get("workflow_params", [])

        workflow = WorkerService.get_workflow_by_name(params=SearchWorkflowByNameParams(name=workflow_name))
        res = WorkerService.queue_workflow(
            params=QueueWorkflowParams(workflow_name=workflow, workflow_params=workflow_params)
        )

        return jsonify({"workflow_id": res}), 201

    def get(self, id: Optional[str] = None) -> ResponseReturnValue:
        if id:
            workflow_params = SearchWorkflowByIdParams(id=id)
            workflow_status = WorkerService.get_workflow_status(params=workflow_params)

            return (jsonify(workflow_status), 200)

        else:
            workflows = WorkerService.get_all_workflows()
            return jsonify({"workflows": workflows}), 200
