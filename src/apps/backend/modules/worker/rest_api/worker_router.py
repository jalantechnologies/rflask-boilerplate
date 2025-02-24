from flask import Blueprint

from modules.worker.rest_api.worker_view import WorkerView


class WorkerRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule("/workers", view_func=WorkerView.as_view("worker_list"), methods=["GET"])
        blueprint.add_url_rule("/workers/<id>", view_func=WorkerView.as_view("worker_status"), methods=["GET"])
        blueprint.add_url_rule("/workers/add", view_func=WorkerView.as_view("worker_add"), methods=["POST"])
        return blueprint
