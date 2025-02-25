import asyncio
import uuid

from temporalio.client import Client
from temporalio.service import RPCError

from modules.config.config_service import ConfigService
from modules.worker.errors import WorkflowIdNotFoundError, WorkflowNameNotFoundError, WorkflowStartError
from modules.worker.types import QueueWorkflowParams, SearchWorkflowByIdParams, SearchWorkflowByNameParams
from workflows import WORKFLOW_MAP


class WorkerService:
    @staticmethod
    async def _get_temporal_workflow_status(params: SearchWorkflowByIdParams) -> dict:
        client = await Client.connect(ConfigService.get_string("TEMPORAL_SERVER_ADDRESS"))
        handle = client.get_workflow_handle(params.id)
        result = await handle.result()
        info = await handle.describe()
        return {
            "workflow_id": info.id,
            "run_id": info.run_id,
            "status": info.status.name if info.status else None,
            "result": result,
            "start_time": str(info.start_time),
            "close_time": str(info.close_time) if info.close_time else None,
            "task_queue": info.task_queue,
            "workflow_type": info.workflow_type,
        }

    @staticmethod
    async def _queue_temporal_workflow(params: QueueWorkflowParams) -> str:
        client = await Client.connect(ConfigService.get_string("TEMPORAL_SERVER_ADDRESS"))
        handle = await client.start_workflow(
            params.workflow_name,
            args=params.workflow_params,
            id=f"{params.workflow_name}-{str(uuid.uuid4())}",
            task_queue=ConfigService.get_string("TEMPORAL_TASK_QUEUE"),
        )
        return handle.id

    @staticmethod
    def get_workflow_by_name(*, params: SearchWorkflowByNameParams) -> str:
        workflow = WORKFLOW_MAP.get(params.name)

        if not workflow:
            raise WorkflowNameNotFoundError(workflow_name=params.name)

        return workflow

    @staticmethod
    def get_workflow_status(*, params: SearchWorkflowByIdParams) -> dict:
        try:
            res = asyncio.run(WorkerService._get_temporal_workflow_status(params=params))

        except RPCError:
            raise WorkflowIdNotFoundError(workflow_id=params.id)

        return res

    @staticmethod
    def get_all_workflows() -> list[str]:
        return list(WORKFLOW_MAP.keys())

    @staticmethod
    def queue_workflow(*, params: QueueWorkflowParams) -> str:
        try:
            workflow_id = asyncio.run(WorkerService._queue_temporal_workflow(params=params))

        except RPCError:
            raise WorkflowStartError(workflow_name=params.workflow_name)

        return workflow_id
