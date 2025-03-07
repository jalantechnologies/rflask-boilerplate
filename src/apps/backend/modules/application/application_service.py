from typing import List, Type

from modules.application.types import RunWorkerAsCronParams, RunWorkerImmediatelyParams, SearchWorkerByIdParams
from modules.application.worker.internal.worker_service import WorkerService
from workers.base_worker import BaseWorker


class ApplicationService:
    @staticmethod
    def connect_client() -> None:
        return WorkerService.connect_client()

    @staticmethod
    def get_worker_details(*, params: SearchWorkerByIdParams) -> dict:
        return WorkerService.get_worker_details(params=params)

    @staticmethod
    def get_all_worker_classes() -> List[Type[BaseWorker]]:
        return WorkerService.get_all_worker_classes()

    @staticmethod
    def run_worker_immediately(*, params: RunWorkerImmediatelyParams) -> str:
        return WorkerService.run_worker_immediately(params=params)

    @staticmethod
    def run_worker_as_cron(*, params: RunWorkerAsCronParams) -> str:
        return WorkerService.run_worker_as_cron(params=params)

    @staticmethod
    def cancel_worker(*, params: SearchWorkerByIdParams) -> None:
        return WorkerService.cancel_worker(params=params)

    @staticmethod
    def terminate_worker(*, params: SearchWorkerByIdParams) -> None:
        return WorkerService.terminate_worker(params=params)
