import asyncio
import uuid
from typing import Any, List, Optional, Tuple, Type

from temporalio.client import Client, WorkflowExecutionStatus, WorkflowHandle
from temporalio.service import RetryConfig, RPCError

from modules.application.errors import (
    WorkerAlreadyCancelledError,
    WorkerAlreadyCompletedError,
    WorkerAlreadyTerminatedError,
    WorkerClientConnectionError,
    WorkerIdNotFoundError,
    WorkerStartError,
)
from modules.application.types import BaseWorker, RegisteredWorker, Worker
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger


class WorkerManager:
    CLIENT: Client
    REGISTERED_WORKERS: List[RegisteredWorker] = []

    @staticmethod
    async def _connect_temporal_server() -> None:
        server_address = ConfigService.get_string("TEMPORAL_SERVER_ADDRESS")
        try:
            WorkerManager.CLIENT = await Client.connect(server_address, retry_config=RetryConfig(max_retries=3))

            Logger.info(message=f"Connected to temporal server at {server_address}")

        except RuntimeError:
            raise WorkerClientConnectionError(server_address=server_address)

    @staticmethod
    async def _get_worker_status(handle: WorkflowHandle) -> Optional[WorkflowExecutionStatus]:
        info = await handle.describe()
        return info.status

    @staticmethod
    async def _start_worker(cls: Type[BaseWorker], arguments: Tuple[Any, ...], cron_schedule: str = "") -> str:
        handle: WorkflowHandle = await WorkerManager.CLIENT.start_workflow(
            cls.__name__,
            args=arguments,
            id=f"{cls.__name__}-{str(uuid.uuid4())}",
            task_queue=cls.priority.value,
            cron_schedule=cron_schedule if cron_schedule else "",
        )
        return handle.id

    @staticmethod
    async def _get_worker_by_id(worker_id: str) -> Worker:
        handle = WorkerManager.CLIENT.get_workflow_handle(worker_id)
        info = await handle.describe()

        return Worker(
            id=info.id,
            status=info.status,
            start_time=info.start_time,
            close_time=info.close_time,
            task_queue=info.task_queue,
            worker_type=info.workflow_type,
        )

    @staticmethod
    async def _run_worker_immediately(cls: Type[BaseWorker], arguments: Tuple[Any, ...]) -> str:
        return await WorkerManager._start_worker(cls, arguments)

    @staticmethod
    async def _schedule_worker_as_cron(cls: Type[BaseWorker], arguments: Tuple[Any, ...], cron_schedule: str) -> str:
        return await WorkerManager._start_worker(cls, arguments, cron_schedule=cron_schedule)

    @staticmethod
    async def _cancel_worker(worker_id: str) -> None:
        handle = WorkerManager.CLIENT.get_workflow_handle(worker_id)

        status = await WorkerManager._get_worker_status(handle)

        if status == WorkflowExecutionStatus.COMPLETED:
            raise WorkerAlreadyCompletedError(worker_id=worker_id)

        if status == WorkflowExecutionStatus.CANCELED:
            raise WorkerAlreadyCancelledError(worker_id=worker_id)

        if status == WorkflowExecutionStatus.TERMINATED:
            raise WorkerAlreadyTerminatedError(worker_id=worker_id)

        await handle.cancel()

    @staticmethod
    async def _terminate_worker(worker_id: str) -> None:
        handle = WorkerManager.CLIENT.get_workflow_handle(worker_id)

        status = await WorkerManager._get_worker_status(handle)

        if status == WorkflowExecutionStatus.COMPLETED:
            raise WorkerAlreadyCompletedError(worker_id=worker_id)

        if status == WorkflowExecutionStatus.CANCELED:
            raise WorkerAlreadyTerminatedError(worker_id=worker_id)

        await handle.terminate()

    @staticmethod
    def register_worker(worker: Type[BaseWorker]) -> None:
        WorkerManager.REGISTERED_WORKERS.append(RegisteredWorker(cls=worker, priority=worker.priority))

    @staticmethod
    def get_all_registered_workers() -> List[RegisteredWorker]:
        return WorkerManager.REGISTERED_WORKERS

    @staticmethod
    def connect_temporal_server() -> None:
        asyncio.run(WorkerManager._connect_temporal_server())

    @staticmethod
    def get_worker_by_id(*, worker_id: str) -> Worker:
        try:
            res = asyncio.run(WorkerManager._get_worker_by_id(worker_id=worker_id))

        except RPCError:
            raise WorkerIdNotFoundError(worker_id=worker_id)

        return res

    @staticmethod
    def run_worker_immediately(*, cls: Type[BaseWorker], arguments: Tuple[Any, ...]) -> str:
        try:
            worker_id = asyncio.run(WorkerManager._run_worker_immediately(cls=cls, arguments=arguments))

        except RPCError:
            raise WorkerStartError(worker_name=cls.__name__)

        return worker_id

    @staticmethod
    def schedule_worker_as_cron(*, cls: Type[BaseWorker], arguments: Tuple[Any, ...], cron_schedule: str) -> str:
        try:
            worker_id = asyncio.run(
                WorkerManager._schedule_worker_as_cron(cls=cls, arguments=arguments, cron_schedule=cron_schedule)
            )

        except RPCError:
            raise WorkerStartError(worker_name=cls.__name__)

        return worker_id

    @staticmethod
    def cancel_worker(*, worker_id: str) -> None:
        try:
            asyncio.run(WorkerManager._cancel_worker(worker_id=worker_id))

        except RPCError:
            raise WorkerIdNotFoundError(worker_id=worker_id)

    @staticmethod
    def terminate_worker(*, worker_id: str) -> None:
        try:
            asyncio.run(WorkerManager._terminate_worker(worker_id=worker_id))

        except RPCError:
            raise WorkerIdNotFoundError(worker_id=worker_id)
