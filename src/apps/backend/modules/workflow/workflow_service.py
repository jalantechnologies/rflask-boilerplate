import asyncio
from typing import Dict

from temporalio.service import RPCError

from modules.workflow.errors import WorkflowIdNotFoundError, WorkflowStartError
from modules.workflow.internal.workflow_manager import WorkflowManager
from modules.workflow.types import QueueWorkflowParams, SearchWorkflowByIdParams
from workflows.workflow_registry import WORKFLOW_MAP


class WorkflowService:
    @staticmethod
    def get_workflow_details(*, params: SearchWorkflowByIdParams) -> dict:
        try:
            res = asyncio.run(WorkflowManager.get_workflow_details(params=params))

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
            workflow_id = asyncio.run(WorkflowManager.queue_workflow(params=params))

        except RPCError:
            raise WorkflowStartError(workflow_name=params.name)

        return workflow_id

    @staticmethod
    def cancel_workflow(*, params: SearchWorkflowByIdParams) -> None:
        try:
            asyncio.run(WorkflowManager.cancel_workflow(params=params))

        except RPCError:
            raise WorkflowIdNotFoundError(workflow_id=params.id)

    @staticmethod
    def terminate_workflow(*, params: SearchWorkflowByIdParams) -> None:
        try:
            asyncio.run(WorkflowManager.terminate_workflow(params=params))

        except RPCError:
            raise WorkflowIdNotFoundError(workflow_id=params.id)
