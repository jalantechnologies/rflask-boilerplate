import asyncio
from typing import List, Type

from temporalio.service import RPCError

from modules.application.worker.errors import (
    WorkerClassInvalidError,
    WorkerIdNotFoundError,
    WorkerStartError,
)
from modules.application.worker.internal.worker_manager import WorkerManager
from modules.application.worker.types import (
    RunWorkerCronParams,
    RunWorkerParams,
    SearchWorkerByIdParams,
)
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
    def get_all_worker_classes() -> List[Type[BaseWorker]]:
        worker_classes = []

        for cls in WORKER_MAP.keys():
            worker_classes.append(cls)

        return worker_classes

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
    def run_worker_cron(*, params: RunWorkerCronParams) -> str:
        if not issubclass(params.cls, BaseWorker) or not hasattr(params.cls, "run"):
            raise WorkerClassInvalidError(
                cls_name=params.cls.__name__, base_cls_name=BaseWorker.__name__
            )

        try:
            worker_id = asyncio.run(WorkerManager.run_worker_cron(params=params))

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
