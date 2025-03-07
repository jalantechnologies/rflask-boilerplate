import asyncio
from typing import Any, Tuple, Type

from temporalio.service import RPCError

from modules.application.errors import WorkerIdNotFoundError, WorkerStartError
from modules.application.types import BaseWorker, Worker
from modules.application.worker.internal.worker_manager import WorkerManager


class WorkerService:
    @staticmethod
    def connect_temporal_server() -> None:
        asyncio.run(WorkerManager.connect_temporal_server())

    @staticmethod
    def get_worker_by_id(*, worker_id: str) -> Worker:
        try:
            res = asyncio.run(WorkerManager.get_worker_by_id(worker_id=worker_id))

        except RPCError:
            raise WorkerIdNotFoundError(worker_id=worker_id)

        return res

    @staticmethod
    def run_worker_immediately(
        *, cls: Type[BaseWorker], arguments: Tuple[Any, ...]
    ) -> str:
        try:
            worker_id = asyncio.run(
                WorkerManager.run_worker_immediately(cls=cls, arguments=arguments)
            )

        except RPCError:
            raise WorkerStartError(worker_name=cls.__name__)

        return worker_id

    @staticmethod
    def schedule_worker_as_cron(
        *, cls: Type[BaseWorker], arguments: Tuple[Any, ...], cron_schedule: str
    ) -> str:
        try:
            worker_id = asyncio.run(
                WorkerManager.schedule_worker_as_cron(
                    cls=cls, arguments=arguments, cron_schedule=cron_schedule
                )
            )

        except RPCError:
            raise WorkerStartError(worker_name=cls.__name__)

        return worker_id

    @staticmethod
    def cancel_worker(*, worker_id: str) -> None:
        try:
            asyncio.run(WorkerManager.cancel_worker(worker_id=worker_id))

        except RPCError:
            raise WorkerIdNotFoundError(worker_id=worker_id)

    @staticmethod
    def terminate_worker(*, worker_id: str) -> None:
        try:
            asyncio.run(WorkerManager.terminate_worker(worker_id=worker_id))

        except RPCError:
            raise WorkerIdNotFoundError(worker_id=worker_id)
