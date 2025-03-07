from dataclasses import asdict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware
from modules.task.errors import (
    DatabaseError,
    TaskBadRequestError,
    TaskCreationError,
    TaskNotFoundError,
    TaskServiceError,
)
from modules.task.internal.task_util import TaskUtil
from modules.task.task_service import TaskService
from modules.task.types import CreateTaskParams


class TaskView(MethodView):
    @access_auth_middleware
    def post(self) -> ResponseReturnValue:
        try:
            request_data = request.get_json()
            task_params = CreateTaskParams(**request_data)

            task = TaskService.create_task(params=task_params)

            task_dict = asdict(task)
            clean_task_dict = {key: TaskUtil.serialize(value) for key, value in task_dict.items()}

            return jsonify(clean_task_dict), 201

        except TaskBadRequestError as e:
            return jsonify({"error": e.message}), e.http_status_code

        except TaskCreationError as e:
            return jsonify({"error": e.message}), e.http_status_code

        except Exception:
            return jsonify({"error": "Internal Server Error"}), 500

    @access_auth_middleware
    def get(self) -> ResponseReturnValue:
        try:
            task_list = TaskService.get_tasks()

            task_dict_list = []
            for task in task_list:
                task_dict = {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at,
                }
                task_dict_list.append(task_dict)

            return jsonify(task_dict_list), 200

        except TaskNotFoundError as e:
            return jsonify({"error": e.message}), e.http_status_code

        except TaskServiceError as e:
            return jsonify({"error": e.message}), e.http_status_code

        except DatabaseError as e:
            return jsonify({"error": "A database error occurred.", "details": str(e)}), e.http_status_code

        except Exception as e:
            return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
