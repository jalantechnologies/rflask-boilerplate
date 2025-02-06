from dataclasses import asdict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware
from modules.task.task_service import TaskService
from modules.task.types import CreateTaskParams, DeleteTaskParams, GetAllTaskParams, UpdateTaskParams


class TaskView(MethodView):

    @access_auth_middleware
    def post(self) -> ResponseReturnValue:
        request_data = request.get_json()
        task_params = CreateTaskParams(account_id=request.account_id, **request_data)
        task = TaskService.create_task(params=task_params)
        task_dict = asdict(task)
        return jsonify(task_dict), 201

    @access_auth_middleware
    def get(self) -> ResponseReturnValue:
        request_args = request.args.to_dict()
        page = int(request_args.get("page", 1)) if "page" in request_args else 1
        size = int(request_args.get("size", "")) if "size" in request_args else None

        task_params = GetAllTaskParams(account_id=request.account_id, page=page, size=size)
        print(task_params)
        tasks = TaskService.get_tasks_for_account(params=task_params)
        task_dicts = [asdict(task) for task in tasks]
        return jsonify(task_dicts), 200

    @access_auth_middleware
    def patch(self, task_id: str) -> ResponseReturnValue:
        request_data = request.get_json()
        update_task_params = UpdateTaskParams(task_id=task_id, account_id=request.account_id, **request_data)
        updated_task = TaskService.update_task_for_account(params=update_task_params)
        updated_task_dict = asdict(updated_task)
        return jsonify(updated_task_dict), 200

    @access_auth_middleware
    def delete(self, task_id: str) -> ResponseReturnValue:
        delete_task_params = DeleteTaskParams(account_id=request.account_id, task_id=task_id)
        is_deleted = TaskService.delete_task_for_account(params=delete_task_params)
        if is_deleted:
            return jsonify({"message": "Task deleted successfully"}), 200
        else:
            return jsonify({"error": "Task not found or could not be deleted"}), 404
