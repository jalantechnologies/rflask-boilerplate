import uuid
from datetime import datetime
from typing import Dict, List, Optional, Union

from temporalio.client import Client, WorkflowExecutionStatus, WorkflowHandle
from temporalio.service import RetryConfig

from modules.application.errors import (
    WorkerAlreadyCancelledError,
    WorkerAlreadyCompletedError,
    WorkerAlreadyTerminatedError,
    WorkerClassNotRegisteredError,
    WorkerClientConnectionError,
)
from modules.application.types import RunWorkerAsCronParams, RunWorkerImmediatelyParams, SearchWorkerByIdParams
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from workers.worker_registry import WORKER_MAP


class WorkerManager:
    CLIENT: Client

    @staticmethod
    async def connect_client() -> None:
        try:
            WorkerManager.CLIENT = await Client.connect(
                ConfigService.get_string("TEMPORAL_SERVER_ADDRESS"), retry_config=RetryConfig(max_retries=3)
            )

            Logger.info(
                message=f"Connected to temporal server at {
                ConfigService.get_string('TEMPORAL_SERVER_ADDRESS')
            }"
            )

        except RuntimeError:
            raise WorkerClientConnectionError(server_address=ConfigService.get_string("TEMPORAL_SERVER_ADDRESS"))

    @staticmethod
    async def _get_worker_status(handle: WorkflowHandle) -> Optional[WorkflowExecutionStatus]:
        info = await handle.describe()
        return info.status

    @staticmethod
    async def _start_worker(params: Union[RunWorkerImmediatelyParams, RunWorkerAsCronParams]) -> str:
        handle: WorkflowHandle = await WorkerManager.CLIENT.start_workflow(
            params.cls.__name__,
            args=params.arguments,
            id=f"{params.cls.__name__}-{str(uuid.uuid4())}",
            task_queue=WORKER_MAP[params.cls].value,
            cron_schedule=params.cron_schedule if isinstance(params, RunWorkerAsCronParams) else "",
        )
        return handle.id

    @staticmethod
    async def get_worker_details(
        params: SearchWorkerByIdParams,
    ) -> Dict[
        str,
        Union[
            str,
            List[Dict[str, Union[str, WorkflowExecutionStatus, datetime, None]]],
            WorkflowExecutionStatus,
            datetime,
            None,
        ],
    ]:
        runs = []

        async for info in WorkerManager.CLIENT.list_workflows(f"WorkflowId = '{params.id}'", limit=params.runs_limit):
            handle = WorkerManager.CLIENT.get_workflow_handle(workflow_id=params.id, run_id=info.run_id)
            info = await handle.describe()

            result = None
            if info.status and info.status == WorkflowExecutionStatus.COMPLETED:
                history = await handle.fetch_history()
                result_event = history.events[-1]
                result_data = result_event.workflow_execution_completed_event_attributes.result.payloads[0].data
                result = result_data.decode("utf-8")

            runs.append(
                {
                    "run_id": info.run_id,
                    "status": info.status,
                    "result": result,
                    "start_time": info.start_time,
                    "close_time": info.close_time,
                }
            )

        handle = WorkerManager.CLIENT.get_workflow_handle(params.id)
        info = await handle.describe()
        return {
            "worker_id": info.id,
            "status": info.status,
            "runs": runs,
            "start_time": info.start_time,
            "close_time": info.close_time,
            "task_queue": info.task_queue,
            "worker_type": info.workflow_type,
        }

    @staticmethod
    async def run_worker_immediately(params: RunWorkerImmediatelyParams) -> str:
        if params.cls not in WORKER_MAP.keys():
            raise WorkerClassNotRegisteredError(cls_name=params.cls.__name__)

        return await WorkerManager._start_worker(params)

    @staticmethod
    async def run_worker_as_cron(params: RunWorkerAsCronParams) -> str:
        if params.cls not in WORKER_MAP.keys():
            raise WorkerClassNotRegisteredError(cls_name=params.cls.__name__)

        return await WorkerManager._start_worker(params)

    @staticmethod
    async def cancel_worker(params: SearchWorkerByIdParams) -> None:
        handle = WorkerManager.CLIENT.get_workflow_handle(params.id)

        status = await WorkerManager._get_worker_status(handle)

        if status == WorkflowExecutionStatus.COMPLETED:
            raise WorkerAlreadyCompletedError(worker_id=params.id)

        if status == WorkflowExecutionStatus.CANCELED:
            raise WorkerAlreadyCancelledError(worker_id=params.id)

        if status == WorkflowExecutionStatus.TERMINATED:
            raise WorkerAlreadyTerminatedError(worker_id=params.id)

        await handle.cancel()

    @staticmethod
    async def terminate_worker(params: SearchWorkerByIdParams) -> None:
        handle = WorkerManager.CLIENT.get_workflow_handle(params.id)

        status = await WorkerManager._get_worker_status(handle)

        if status == WorkflowExecutionStatus.COMPLETED:
            raise WorkerAlreadyCompletedError(worker_id=params.id)

        if status == WorkflowExecutionStatus.CANCELED:
            raise WorkerAlreadyTerminatedError(worker_id=params.id)

        await handle.terminate()
