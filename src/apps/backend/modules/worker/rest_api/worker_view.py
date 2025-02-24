from typing import Optional

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.worker.types import QueueTaskParams, SearchTaskByIdParams, SearchTaskByNameParams
from modules.worker.worker_service import WorkerService


class WorkerView(MethodView):
    def post(self) -> ResponseReturnValue:
        """
        Expected request body:

        {
            "task_name": "tasks.XYZ",
            "task_params": {
                "x": ...,
                "y": ...
            }
        }
        """

        request_data = request.get_json()

        task_name = request_data.get("task_name")
        task_params = request_data.get("task_params") or None

        task = WorkerService.get_task_by_name(params=SearchTaskByNameParams(name=task_name))
        res = WorkerService.queue_task(params=QueueTaskParams(task=task, task_params=task_params))

        return jsonify({"task_id": res.id}), 201

    def get(self, id: Optional[str] = None) -> ResponseReturnValue:
        if id:
            task_params = SearchTaskByIdParams(id=id)
            task_status = WorkerService.get_task_status(params=task_params)

            return (
                jsonify(
                    {
                        "task_id": task_status.id,
                        "task_status": task_status.status,
                        "task_result": task_status.result if task_status.ready() else None,
                    }
                ),
                200,
            )

        else:
            tasks = WorkerService.get_all_tasks()
            return jsonify({"tasks": tasks}), 200
