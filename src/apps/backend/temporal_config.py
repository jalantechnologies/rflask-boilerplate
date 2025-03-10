from typing import List, Type

from temporalio import workflow

from modules.application.types import BaseWorker, RegisteredWorker
from modules.application.workers.health_check_worker import HealthCheckWorker


class TemporalConfig:
    WORKERS: List[Type[BaseWorker]] = [
        HealthCheckWorker,
    ]

    REGISTERED_WORKERS: List[RegisteredWorker] = []

    @staticmethod
    def _register_worker(cls: Type[BaseWorker]) -> None:
        # Wrap the run() method so Temporal recognizes it as the application entry point.
        wrapped_run = workflow.run(cls.run)
        setattr(cls, "run", wrapped_run)

        # Decorate the class itself as a application definition.
        cls = workflow.defn(cls)

        TemporalConfig.REGISTERED_WORKERS.append(
            RegisteredWorker(cls=cls, priority=cls.priority)
        )

    @staticmethod
    def mount_workers() -> None:
        for worker in TemporalConfig.WORKERS:
            TemporalConfig._register_worker(worker)

    @staticmethod
    def get_all_registered_workers() -> List[RegisteredWorker]:
        return TemporalConfig.REGISTERED_WORKERS
