import time

import pytest
from modules.workflow.errors import WorkflowIdNotFoundError, WorkflowNameNotFoundError
from modules.workflow.types import (
    QueueWorkflowParams,
    SearchWorkflowByIdParams,
    WorkflowPriority,
)
from modules.workflow.workflow_service import WorkflowService
from temporalio.client import WorkflowExecutionStatus

from tests.modules.workflow.base_test_workflow import BaseTestWorkflow


class TestWorkflowService(BaseTestWorkflow):
    def test_get_all_workflows(self) -> None:
        workflows_list = WorkflowService.get_all_workflows()
        assert {
            "name": "TestDefaultWorkflow",
            "priority": WorkflowPriority.DEFAULT,
        } in workflows_list

    def test_queue_and_get_details_workflow(self) -> None:
        queue_params = QueueWorkflowParams(
            name="TestDefaultWorkflow", arguments=[10, 5], cron_schedule=""
        )
        workflow_id = WorkflowService.queue_workflow(params=queue_params)
        assert workflow_id

        time.sleep(1)

        details_params = SearchWorkflowByIdParams(id=workflow_id)
        data = WorkflowService.get_workflow_details(params=details_params)
        assert data["workflow_id"] == workflow_id
        assert int(data["runs"][0]["result"]) == 15
        assert data["status"] == WorkflowExecutionStatus.COMPLETED

    def test_queue_workflow_with_invalid_name(self) -> None:
        queue_params = QueueWorkflowParams(
            name="non_existent", arguments=[10, 5], cron_schedule=""
        )
        with pytest.raises(WorkflowNameNotFoundError):
            WorkflowService.queue_workflow(params=queue_params)

    def test_get_details_with_invalid_workflow_id(self) -> None:
        status_params = SearchWorkflowByIdParams(id="non_existent")
        with pytest.raises(WorkflowIdNotFoundError):
            WorkflowService.get_workflow_details(params=status_params)
