import time

import pytest
from temporalio.client import WorkflowExecutionStatus
from tests.modules.application.base_test_application import BaseTestApplication
from tests.modules.application.mock_workers import MockDefaultWorker

from modules.application.application_service import ApplicationService
from modules.application.errors import WorkerIdNotFoundError


class TestWorkerService(BaseTestApplication):
    def test_run_worker_and_get_details(self) -> None:
        worker_id = ApplicationService.run_worker_immediately(
            cls=MockDefaultWorker, arguments=("Hello, world!",)
        )
        assert worker_id

        time.sleep(1)

        worker_details = ApplicationService.get_worker_by_id(worker_id=worker_id)
        assert worker_details.id == worker_id
        assert worker_details.status == WorkflowExecutionStatus.COMPLETED

    def test_get_details_with_invalid_worker_id(self) -> None:
        with pytest.raises(WorkerIdNotFoundError):
            ApplicationService.get_worker_by_id(worker_id="invalid_id")
