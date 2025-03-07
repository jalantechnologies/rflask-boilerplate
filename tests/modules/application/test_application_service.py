import time

import pytest
from temporalio.client import WorkflowExecutionStatus
from tests.modules.application.base_test_application import BaseTestApplication

from modules.application.application_service import ApplicationService
from modules.application.errors import WorkerIdNotFoundError, WorkerNotRegisteredError
from modules.application.types import BaseWorker
from modules.application.workers.health_check_worker import HealthCheckWorker


class TestWorkerService(BaseTestApplication):
    def test_run_worker_immediately(self) -> None:
        worker_id = ApplicationService.run_worker_immediately(cls=HealthCheckWorker)
        assert worker_id

        time.sleep(1)

        worker_details = ApplicationService.get_worker_by_id(worker_id=worker_id)
        assert worker_details.id == worker_id
        assert worker_details.status == WorkflowExecutionStatus.COMPLETED

    def test_schedule_worker_as_cron(self) -> None:
        worker_id = ApplicationService.schedule_worker_as_cron(
            cls=HealthCheckWorker, cron_schedule="*/1 * * * *"
        )
        assert worker_id

        worker_details = ApplicationService.get_worker_by_id(worker_id=worker_id)
        assert worker_details.id == worker_id
        assert worker_details.status == WorkflowExecutionStatus.RUNNING

        ApplicationService.terminate_worker(worker_id=worker_id)

        time.sleep(1)

        worker_details = ApplicationService.get_worker_by_id(worker_id=worker_id)
        assert worker_details.id == worker_id
        assert worker_details.status == WorkflowExecutionStatus.TERMINATED

    def test_run_worker_with_unregistered_worker(self) -> None:
        class UnRegisteredWorker(BaseWorker):
            def run(self) -> None: ...

        with pytest.raises(WorkerNotRegisteredError):
            ApplicationService.run_worker_immediately(cls=UnRegisteredWorker)

    def test_get_details_with_invalid_worker_id(self) -> None:
        with pytest.raises(WorkerIdNotFoundError):
            ApplicationService.get_worker_by_id(worker_id="invalid_id")
