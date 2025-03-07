import time

import pytest
from temporalio.client import WorkflowExecutionStatus
from tests.modules.application.base_test_application import BaseTestApplication

from modules.application.application_service import ApplicationService
from modules.application.worker.errors import (
    WorkerClassInvalidError,
    WorkerClassNotRegisteredError,
    WorkerIdNotFoundError,
)
from modules.application.worker.types import (
    RunWorkerImmediatelyParams,
    SearchWorkerByIdParams,
)
from workers.base_worker import BaseWorker
from workers.dummy_workers import TestDefaultWorker


class TestWorkerService(BaseTestApplication):
    def test_get_all_worker_classes(self) -> None:
        worker_class_list = ApplicationService.get_all_worker_classes()
        assert TestDefaultWorker in worker_class_list

    def test_run_worker_and_get_details(self) -> None:
        run_params = RunWorkerImmediatelyParams(TestDefaultWorker, arguments=[10, 5])
        worker_id = ApplicationService.run_worker_immediately(params=run_params)
        assert worker_id

        time.sleep(1)

        details_params = SearchWorkerByIdParams(id=worker_id)
        data = ApplicationService.get_worker_details(params=details_params)
        assert data["worker_id"] == worker_id
        assert int(data["runs"][0]["result"]) == 15
        assert data["status"] == WorkflowExecutionStatus.COMPLETED

    def test_run_worker_with_invalid_class(self) -> None:
        class InvalidWorker: ...

        run_params = RunWorkerImmediatelyParams(InvalidWorker, arguments=[10, 5])
        with pytest.raises(WorkerClassInvalidError):
            ApplicationService.run_worker_immediately(params=run_params)

    def test_run_unregistered_worker(self) -> None:
        class NonExistentWorker(BaseWorker):
            async def run(self) -> None: ...

        run_params = RunWorkerImmediatelyParams(NonExistentWorker, arguments=[10, 5])
        with pytest.raises(WorkerClassNotRegisteredError):
            ApplicationService.run_worker_immediately(params=run_params)

    def test_get_details_with_invalid_worker_id(self) -> None:
        status_params = SearchWorkerByIdParams(id="non_existent")
        with pytest.raises(WorkerIdNotFoundError):
            ApplicationService.get_worker_details(params=status_params)
