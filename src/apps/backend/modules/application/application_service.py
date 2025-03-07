from modules.application.types import (
    RunWorkerAsCronParams,
    RunWorkerImmediatelyParams,
    Worker,
)
from modules.application.worker.internal.worker_service import WorkerService


class ApplicationService:
    @staticmethod
    def connect_temporal_server() -> None:
        return WorkerService.connect_temporal_server()

    @staticmethod
    def get_worker_by_id(*, worker_id: str) -> Worker:
        return WorkerService.get_worker_by_id(worker_id=worker_id)

    @staticmethod
    def run_worker_immediately(*, params: RunWorkerImmediatelyParams) -> str:
        return WorkerService.run_worker_immediately(params=params)

    @staticmethod
    def run_worker_as_cron(*, params: RunWorkerAsCronParams) -> str:
        return WorkerService.schedule_worker_as_cron(params=params)

    @staticmethod
    def cancel_worker(*, worker_id: str) -> None:
        return WorkerService.cancel_worker(worker_id=worker_id)

    @staticmethod
    def terminate_worker(*, worker_id: str) -> None:
        return WorkerService.terminate_worker(worker_id=worker_id)
