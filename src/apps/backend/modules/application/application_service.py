from typing import Dict

from modules.application.worker.internal.worker_service import WorkerService
from modules.application.worker.types import (
    RunWorkerCronParams,
    RunWorkerParams,
    SearchWorkerByIdParams,
)


class ApplicationService:
    @staticmethod
    def get_worker_details(*, params: SearchWorkerByIdParams) -> dict:
        return WorkerService.get_worker_details(params=params)

    @staticmethod
    def get_all_workers() -> list[Dict[str, object]]:
        return WorkerService.get_all_workers()

    @staticmethod
    def run_worker(*, params: RunWorkerParams) -> str:
        return WorkerService.run_worker(params=params)

    @staticmethod
    def run_worker_cron(*, params: RunWorkerCronParams) -> str:
        return WorkerService.run_worker_cron(params=params)

    @staticmethod
    def cancel_worker(*, params: SearchWorkerByIdParams) -> None:
        return WorkerService.cancel_worker(params=params)

    @staticmethod
    def terminate_worker(*, params: SearchWorkerByIdParams) -> None:
        return WorkerService.terminate_worker(params=params)
