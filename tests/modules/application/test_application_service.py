import time

import pytest
from temporalio.client import WorkflowExecutionStatus
from tests.modules.application.base_test_application import BaseTestApplication

from modules.application.application_service import ApplicationService
from modules.application.errors import (
    WorkerClassInvalidError,
    WorkerClassNotRegisteredError,
    WorkerIdNotFoundError,
)
from modules.application.types import BaseWorker, RunWorkerImmediatelyParams
from workers.dummy_workers import TestDefaultWorker


class TestWorkerService(BaseTestApplication):
    def test_run_worker_and_get_details(self) -> None:
        run_params = RunWorkerImmediatelyParams(
            TestDefaultWorker, arguments=("Hello, world!",)
        )
        worker_id = ApplicationService.run_worker_immediately(params=run_params)
        assert worker_id

        time.sleep(1)

        worker_details = ApplicationService.get_worker_by_id(worker_id=worker_id)
        assert worker_details.id == worker_id
        assert worker_details.status == WorkflowExecutionStatus.COMPLETED

    def test_run_worker_with_invalid_class(self) -> None:
        class InvalidWorker: ...

        run_params = RunWorkerImmediatelyParams(
            InvalidWorker, arguments=("Hello, world!",)
        )
        with pytest.raises(WorkerClassInvalidError):
            ApplicationService.run_worker_immediately(params=run_params)

    def test_run_unregistered_worker(self) -> None:
        class NonExistentWorker(BaseWorker):
            async def run(self) -> None: ...

        run_params = RunWorkerImmediatelyParams(
            NonExistentWorker, arguments=("Hello, world!",)
        )
        with pytest.raises(WorkerClassNotRegisteredError):
            ApplicationService.run_worker_immediately(params=run_params)

    def test_get_details_with_invalid_worker_id(self) -> None:
        with pytest.raises(WorkerIdNotFoundError):
            ApplicationService.get_worker_by_id(worker_id="invalid_id")
