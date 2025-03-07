import asyncio

from temporalio.service import RPCError

from modules.application.errors import (
    WorkerClassInvalidError,
    WorkerIdNotFoundError,
    WorkerStartError,
)
from modules.application.types import (
    BaseWorker,
    RunWorkerAsCronParams,
    RunWorkerImmediatelyParams,
    Worker,
)
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
    def run_worker_immediately(*, params: RunWorkerImmediatelyParams) -> str:
        if not issubclass(params.cls, BaseWorker) or not hasattr(params.cls, "run"):
            raise WorkerClassInvalidError(
                cls_name=params.cls.__name__, base_cls_name=BaseWorker.__name__
            )

        try:
            worker_id = asyncio.run(WorkerManager.run_worker_immediately(params=params))

        except RPCError:
            raise WorkerStartError(worker_name=params.cls.__name__)

        return worker_id

    @staticmethod
    def schedule_worker_as_cron(*, params: RunWorkerAsCronParams) -> str:
        if not issubclass(params.cls, BaseWorker) or not hasattr(params.cls, "run"):
            raise WorkerClassInvalidError(
                cls_name=params.cls.__name__, base_cls_name=BaseWorker.__name__
            )

        try:
            worker_id = asyncio.run(
                WorkerManager.schedule_worker_as_cron(params=params)
            )

        except RPCError:
            raise WorkerStartError(worker_name=params.cls.__name__)

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
