from dataclasses import asdict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware
from modules.task.task_service import TaskService
from modules.task.types import CreateTaskParams, TaskSearchByIdParams, UpdateTaskParams


class TaskView(MethodView):
    def post(self) -> ResponseReturnValue:
        request_data = request.get_json()
        task_params = CreateTaskParams(**request_data)
        task = TaskService.create_task(params=task_params)
        task_dict = asdict(task)
        return jsonify(task_dict), 201

    @access_auth_middleware
    def get(self, id: str) -> ResponseReturnValue:
        task_params = TaskSearchByIdParams(id=id)
        task = TaskService.get_task_by_id(params=task_params)
        task_dict = asdict(task)
        return jsonify(task_dict), 200

    def patch(self, id: str) -> ResponseReturnValue:
        request_data = request.get_json()
        update_task_params = UpdateTaskParams(task_id=id, **request_data)
        task = TaskService.update_task(params=update_task_params)
        task_dict = asdict(task)
        return jsonify(task_dict), 200
