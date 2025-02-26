import pytest
from modules.workflow.errors import WorkflowIdNotFoundError, WorkflowNameNotFoundError
from modules.workflow.types import (
    QueueWorkflowParams,
    SearchWorkflowByIdParams,
    SearchWorkflowByNameParams,
)
from modules.workflow.workflow_service import WorkflowService

from tests.modules.workflow.base_test_workflow import BaseTestWorkflow


class TestWorkflowService(BaseTestWorkflow):
    def test_get_workflow_by_name(self) -> None:
        params = SearchWorkflowByNameParams(name="add")
        workflow = WorkflowService.get_workflow_by_name(params=params)
        assert workflow == "AddWorkflow"

    def test_get_workflow_by_invalid_name(self) -> None:
        params = SearchWorkflowByNameParams(name="non_existent")
        with pytest.raises(WorkflowNameNotFoundError):
            WorkflowService.get_workflow_by_name(params=params)

    def test_get_all_workflows(self) -> None:
        workflows_list = WorkflowService.get_all_workflows()
        assert "add" in workflows_list

    def test_queue_and_get_status(self) -> None:
        queue_params = QueueWorkflowParams(
            workflow_name="AddWorkflow", workflow_params=[10, 5]
        )
        workflow_id = WorkflowService.queue_workflow(params=queue_params)
        assert isinstance(workflow_id, str) and len(workflow_id) > 0

        status_params = SearchWorkflowByIdParams(id=workflow_id)
        status = WorkflowService.get_workflow_status(params=status_params)
        assert status["workflow_id"] == workflow_id
        assert status["result"] == 15
        assert status["status"] == "COMPLETED"

    def test_get_status_with_invalid_workflow_id(self) -> None:
        status_params = SearchWorkflowByIdParams(id="non_existent")
        with pytest.raises(WorkflowIdNotFoundError):
            WorkflowService.get_workflow_status(params=status_params)
