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
    SearchWorkerByIdParams,
)
from modules.application.worker.internal.worker_manager import WorkerManager


class WorkerService:
    @staticmethod
    def connect_client() -> None:
        asyncio.run(WorkerManager.connect_client())

    @staticmethod
    def get_worker_details(*, params: SearchWorkerByIdParams) -> dict:
        try:
            res = asyncio.run(WorkerManager.get_worker_details(params=params))

        except RPCError:
            raise WorkerIdNotFoundError(worker_id=params.id)

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
    def cancel_worker(*, params: SearchWorkerByIdParams) -> None:
        try:
            asyncio.run(WorkerManager.cancel_worker(params=params))

        except RPCError:
            raise WorkerIdNotFoundError(worker_id=params.id)

    @staticmethod
    def terminate_worker(*, params: SearchWorkerByIdParams) -> None:
        try:
            asyncio.run(WorkerManager.terminate_worker(params=params))

        except RPCError:
            raise WorkerIdNotFoundError(worker_id=params.id)
