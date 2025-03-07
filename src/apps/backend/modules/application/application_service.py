import os
import sys
from typing import Any, Dict, Tuple, Type

from modules.application.internal.worker_manager import WorkerManager
from modules.application.types import BaseWorker, Worker, WorkerPriority


class ApplicationService:
    @staticmethod
    def register_worker(worker: Type[BaseWorker]) -> None:
        return WorkerManager.register_worker(worker)

    @staticmethod
    def get_all_registered_workers() -> Dict[Type[BaseWorker], WorkerPriority]:
        return WorkerManager.get_all_registered_workers()

    @staticmethod
    def connect_temporal_server() -> None:
        return WorkerManager.connect_temporal_server()

    @staticmethod
    def get_worker_by_id(*, worker_id: str) -> Worker:
        return WorkerManager.get_worker_by_id(worker_id=worker_id)

    @staticmethod
    def run_worker_immediately(*, cls: Type[BaseWorker], arguments: Tuple[Any, ...]) -> str:
        return WorkerManager.run_worker_immediately(cls=cls, arguments=arguments)

    @staticmethod
    def run_worker_as_cron(*, cls: Type[BaseWorker], arguments: Tuple[Any, ...], cron_schedule: str) -> str:
        return WorkerManager.schedule_worker_as_cron(cls=cls, arguments=arguments, cron_schedule=cron_schedule)

    @staticmethod
    def cancel_worker(*, worker_id: str) -> None:
        return WorkerManager.cancel_worker(worker_id=worker_id)

    @staticmethod
    def terminate_worker(*, worker_id: str) -> None:
        return WorkerManager.terminate_worker(worker_id=worker_id)


# Import mock workers for testing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../..")))
from tests.modules.application import mock_workers  # noqa: F401
