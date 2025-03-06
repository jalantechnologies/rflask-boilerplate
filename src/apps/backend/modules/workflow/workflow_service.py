import asyncio
import uuid
from typing import Dict, Optional

from temporalio.client import Client, WorkflowExecutionStatus, WorkflowHandle
from temporalio.service import RetryConfig, RPCError

from modules.config.config_service import ConfigService
from modules.workflow.errors import (
    WorkflowAlreadyCancelledError,
    WorkflowAlreadyCompletedError,
    WorkflowAlreadyTerminatedError,
    WorkflowClientConnectionError,
    WorkflowIdNotFoundError,
    WorkflowNameNotFoundError,
    WorkflowStartError,
)
from modules.workflow.types import QueueWorkflowParams, SearchWorkflowByIdParams
from workflows.workflow_registry import WORKFLOW_MAP


class WorkflowService:
    CLIENT: Optional[Client] = None

    @staticmethod
    async def _get_client() -> Client:
        if not WorkflowService.CLIENT:
            try:
                WorkflowService.CLIENT = await Client.connect(
                    ConfigService.get_string("TEMPORAL_SERVER_ADDRESS"), retry_config=RetryConfig(max_retries=3)
                )

            except RuntimeError:
                raise WorkflowClientConnectionError(server_address=ConfigService.get_string("TEMPORAL_SERVER_ADDRESS"))

        return WorkflowService.CLIENT

    @staticmethod
    async def _get_workflow_status(handle: WorkflowHandle) -> WorkflowExecutionStatus:
        info = await handle.describe()
        return info.status

    @staticmethod
    async def _get_workflow_details(params: SearchWorkflowByIdParams) -> dict:
        client = await WorkflowService._get_client()

        runs = []

        async for info in client.list_workflows(f"WorkflowId = '{params.id}'", limit=params.runs_limit):
            handle = client.get_workflow_handle(workflow_id=params.id, run_id=info.run_id)
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
                    "status": info.status.name,
                    "result": result,
                    "start_time": info.start_time,
                    "close_time": info.close_time,
                }
            )

        handle = client.get_workflow_handle(params.id)
        info = await handle.describe()
        return {
            "workflow_id": info.id,
            "status": info.status,
            "runs": runs,
            "start_time": info.start_time,
            "close_time": info.close_time,
            "task_queue": info.task_queue,
            "workflow_type": info.workflow_type,
        }

    @staticmethod
    async def _queue_workflow(params: QueueWorkflowParams) -> str:
        client = await WorkflowService._get_client()

        if params.name not in WORKFLOW_MAP.keys():
            raise WorkflowNameNotFoundError(workflow_name=params.name)

        handle = await client.start_workflow(
            params.name,
            args=params.arguments,
            cron_schedule=params.cron_schedule,
            id=f"{params.name}-{str(uuid.uuid4())}",
            task_queue=WORKFLOW_MAP[params.name]["priority"].value,
        )
        return handle.id

    @staticmethod
    async def _cancel_workflow(params: SearchWorkflowByIdParams) -> None:
        client = await WorkflowService._get_client()
        handle = client.get_workflow_handle(params.id)

        if await WorkflowService._get_workflow_status(handle) == WorkflowExecutionStatus.COMPLETED:
            raise WorkflowAlreadyCompletedError(workflow_id=params.id)

        if await WorkflowService._get_workflow_status(handle) == WorkflowExecutionStatus.CANCELED:
            raise WorkflowAlreadyCancelledError(workflow_id=params.id)

        if await WorkflowService._get_workflow_status(handle) == WorkflowExecutionStatus.TERMINATED:
            raise WorkflowAlreadyTerminatedError(workflow_id=params.id)

        await handle.cancel()

    @staticmethod
    async def _terminate_workflow(params: SearchWorkflowByIdParams) -> None:
        client = await WorkflowService._get_client()
        handle = client.get_workflow_handle(params.id)

        if await WorkflowService._get_workflow_status(handle) == WorkflowExecutionStatus.COMPLETED:
            raise WorkflowAlreadyCompletedError(workflow_id=params.id)

        if await WorkflowService._get_workflow_status(handle) == WorkflowExecutionStatus.CANCELED:
            raise WorkflowAlreadyTerminatedError(workflow_id=params.id)

        await handle.terminate()

    @staticmethod
    def get_workflow_details(*, params: SearchWorkflowByIdParams) -> dict:
        try:
            res = asyncio.run(WorkflowService._get_workflow_details(params=params))

        except RPCError:
            raise WorkflowIdNotFoundError(workflow_id=params.id)

        return res

    @staticmethod
    def get_all_workflows() -> list[Dict[str, str]]:
        workflows = []

        for name, details in WORKFLOW_MAP.items():
            workflows.append({"name": name, "priority": details["priority"]})

        return workflows

    @staticmethod
    def queue_workflow(*, params: QueueWorkflowParams) -> str:
        try:
            workflow_id = asyncio.run(WorkflowService._queue_workflow(params=params))

        except RPCError:
            raise WorkflowStartError(workflow_name=params.name)

        return workflow_id

    @staticmethod
    def cancel_workflow(*, params: SearchWorkflowByIdParams) -> None:
        try:
            asyncio.run(WorkflowService._cancel_workflow(params=params))

        except RPCError:
            raise WorkflowIdNotFoundError(workflow_id=params.id)

    @staticmethod
    def terminate_workflow(*, params: SearchWorkflowByIdParams) -> None:
        try:
            asyncio.run(WorkflowService._terminate_workflow(params=params))

        except RPCError:
            raise WorkflowIdNotFoundError(workflow_id=params.id)
