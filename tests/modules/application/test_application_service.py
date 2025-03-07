import time

import pytest
from temporalio.client import WorkflowExecutionStatus
from tests.modules.application.base_test_application import BaseTestApplication

from modules.application.application_service import ApplicationService
from modules.application.errors import WorkerIdNotFoundError
from workers.dummy_workers import TestDefaultWorker


class TestWorkerService(BaseTestApplication):
    def test_run_worker_and_get_details(self) -> None:
        worker_id = ApplicationService.run_worker_immediately(
            cls=TestDefaultWorker, arguments=("Hello, world!",)
        )
        assert worker_id

        time.sleep(1)

        worker_details = ApplicationService.get_worker_by_id(worker_id=worker_id)
        assert worker_details.id == worker_id
        assert worker_details.status == WorkflowExecutionStatus.COMPLETED

    def test_get_details_with_invalid_worker_id(self) -> None:
        with pytest.raises(WorkerIdNotFoundError):
            ApplicationService.get_worker_by_id(worker_id="invalid_id")
