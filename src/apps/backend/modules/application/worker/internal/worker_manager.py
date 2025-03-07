import uuid
from typing import Optional, Union

from temporalio.client import Client, WorkflowExecutionStatus, WorkflowHandle
from temporalio.service import RetryConfig

from modules.application.errors import (
    WorkerAlreadyCancelledError,
    WorkerAlreadyCompletedError,
    WorkerAlreadyTerminatedError,
    WorkerClassNotRegisteredError,
    WorkerClientConnectionError,
)
from modules.application.types import (
    RunWorkerAsCronParams,
    RunWorkerImmediatelyParams,
    Worker,
)
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from workers.worker_registry import WORKER_MAP


class WorkerManager:
    CLIENT: Client

    @staticmethod
    async def connect_temporal_server() -> None:
        server_address = ConfigService.get_string("TEMPORAL_SERVER_ADDRESS")
        try:
            WorkerManager.CLIENT = await Client.connect(
                server_address, retry_config=RetryConfig(max_retries=3)
            )

            Logger.info(message=f"Connected to temporal server at {server_address}")

        except RuntimeError:
            raise WorkerClientConnectionError(server_address=server_address)

    @staticmethod
    async def _get_worker_status(
        handle: WorkflowHandle,
    ) -> Optional[WorkflowExecutionStatus]:
        info = await handle.describe()
        return info.status

    @staticmethod
    async def _start_worker(
        params: Union[RunWorkerImmediatelyParams, RunWorkerAsCronParams],
        cron_schedule: str = "",
    ) -> str:
        handle: WorkflowHandle = await WorkerManager.CLIENT.start_workflow(
            params.cls.__name__,
            args=params.arguments,
            id=f"{params.cls.__name__}-{str(uuid.uuid4())}",
            task_queue=WORKER_MAP[params.cls].value,
            cron_schedule=cron_schedule if cron_schedule else "",
        )
        return handle.id

    @staticmethod
    async def get_worker_by_id(
        worker_id: str,
    ) -> Worker:
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
    async def run_worker_immediately(params: RunWorkerImmediatelyParams) -> str:
        if params.cls not in WORKER_MAP.keys():
            raise WorkerClassNotRegisteredError(cls_name=params.cls.__name__)

        return await WorkerManager._start_worker(params)

    @staticmethod
    async def schedule_worker_as_cron(params: RunWorkerAsCronParams) -> str:
        if params.cls not in WORKER_MAP.keys():
            raise WorkerClassNotRegisteredError(cls_name=params.cls.__name__)

        return await WorkerManager._start_worker(
            params, cron_schedule=params.cron_schedule
        )

    @staticmethod
    async def cancel_worker(worker_id: str) -> None:
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
    async def terminate_worker(worker_id: str) -> None:
        handle = WorkerManager.CLIENT.get_workflow_handle(worker_id)

        status = await WorkerManager._get_worker_status(handle)

        if status == WorkflowExecutionStatus.COMPLETED:
            raise WorkerAlreadyCompletedError(worker_id=worker_id)

        if status == WorkflowExecutionStatus.CANCELED:
            raise WorkerAlreadyTerminatedError(worker_id=worker_id)

        await handle.terminate()
