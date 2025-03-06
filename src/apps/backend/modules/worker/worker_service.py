import asyncio
from typing import Dict

from temporalio.service import RPCError

from modules.worker.errors import (
    WorkerClassInvalidError,
    WorkerIdNotFoundError,
    WorkerStartError,
)
from modules.worker.internal.worker_manager import WorkerManager
from modules.worker.types import RunWorkerParams, SearchWorkerByIdParams
from workers.base_worker import BaseWorker
from workers.worker_registry import WORKER_MAP


class WorkerService:
    @staticmethod
    def get_worker_details(*, params: SearchWorkerByIdParams) -> dict:
        try:
            res = asyncio.run(WorkerManager.get_worker_details(params=params))

        except RPCError:
            raise WorkerIdNotFoundError(worker_id=params.id)

        return res

    @staticmethod
    def get_all_workers() -> list[Dict[str, object]]:
        workers = []

        for cls, priority in WORKER_MAP.items():
            workers.append({"name": cls, "priority": priority})

        return workers

    @staticmethod
    def run_worker(*, params: RunWorkerParams) -> str:
        if not issubclass(params.cls, BaseWorker) or not hasattr(params.cls, "run"):
            raise WorkerClassInvalidError(
                cls_name=params.cls.__name__, base_cls_name=BaseWorker.__name__
            )

        try:
            worker_id = asyncio.run(WorkerManager.run_worker(params=params))

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
