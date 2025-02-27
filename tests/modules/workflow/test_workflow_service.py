import pytest
from tests.modules.workflow.base_test_workflow import BaseTestWorkflow

from modules.workflow.errors import WorkflowIdNotFoundError, WorkflowNameNotFoundError
from modules.workflow.types import QueueWorkflowParams, SearchWorkflowByIdParams
from modules.workflow.workflow_service import WorkflowService


class TestWorkflowService(BaseTestWorkflow):
    def test_get_all_workflows(self) -> None:
        workflows_list = WorkflowService.get_all_workflows()
        assert "AddWorkflow" in workflows_list

    def test_queue_and_get_status(self) -> None:
        queue_params = QueueWorkflowParams(
            name="AddWorkflow", arguments=[10, 5], priority="DEFAULT", cron_schedule=""
        )
        workflow_id = WorkflowService.queue_workflow(params=queue_params)
        assert isinstance(workflow_id, str) and len(workflow_id) > 0

        status_params = SearchWorkflowByIdParams(id=workflow_id)
        status = WorkflowService.get_workflow_status(params=status_params)
        assert status["workflow_id"] == workflow_id
        assert status["result"] == 15
        assert status["status"] == "COMPLETED"

    def test_queue_workflow_with_invalid_name(self) -> None:
        queue_params = QueueWorkflowParams(
            name="non_existent", arguments=[10, 5], priority="DEFAULT", cron_schedule=""
        )
        with pytest.raises(WorkflowNameNotFoundError):
            WorkflowService.queue_workflow(params=queue_params)

    def test_get_status_with_invalid_workflow_id(self) -> None:
        status_params = SearchWorkflowByIdParams(id="non_existent")
        with pytest.raises(WorkflowIdNotFoundError):
            WorkflowService.get_workflow_status(params=status_params)
