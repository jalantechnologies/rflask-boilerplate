from flask import Blueprint

from modules.worker.rest_api.worker_router import WorkerRouter


class WorkerRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        worker_api_blueprint = Blueprint("worker", __name__)
        return WorkerRouter.create_route(blueprint=worker_api_blueprint)
