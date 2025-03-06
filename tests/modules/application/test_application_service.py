import time

import pytest
from modules.application.application_service import ApplicationService
from modules.application.worker.errors import (
    WorkerClassInvalidError,
    WorkerClassNotRegisteredError,
    WorkerIdNotFoundError,
)
from modules.application.worker.types import (
    RunWorkerParams,
    SearchWorkerByIdParams,
    WorkerPriority,
)
from temporalio.client import WorkflowExecutionStatus
from workers.base_worker import BaseWorker
from workers.dummy_workers import TestDefaultWorker

from tests.modules.application.base_test_application import BaseTestApplication


class TestWorkerService(BaseTestApplication):
    def test_get_all_workers(self) -> None:
        workers_list = ApplicationService.get_all_workers()
        assert {
            "name": TestDefaultWorker,
            "priority": WorkerPriority.DEFAULT,
        } in workers_list

    def test_run_worker_and_get_details(self) -> None:
        run_params = RunWorkerParams(TestDefaultWorker, arguments=[10, 5])
        worker_id = ApplicationService.run_worker(params=run_params)
        assert worker_id

        time.sleep(1)

        details_params = SearchWorkerByIdParams(id=worker_id)
        data = ApplicationService.get_worker_details(params=details_params)
        assert data["worker_id"] == worker_id
        assert int(data["runs"][0]["result"]) == 15
        assert data["status"] == WorkflowExecutionStatus.COMPLETED

    def test_run_worker_with_invalid_class(self) -> None:
        class InvalidWorker: ...

        run_params = RunWorkerParams(InvalidWorker, arguments=[10, 5])
        with pytest.raises(WorkerClassInvalidError):
            ApplicationService.run_worker(params=run_params)

    def test_run_unregistered_worker(self) -> None:
        class NonExistentWorker(BaseWorker):
            async def run(self) -> None: ...

        run_params = RunWorkerParams(NonExistentWorker, arguments=[10, 5])
        with pytest.raises(WorkerClassNotRegisteredError):
            ApplicationService.run_worker(params=run_params)

    def test_get_details_with_invalid_worker_id(self) -> None:
        status_params = SearchWorkerByIdParams(id="non_existent")
        with pytest.raises(WorkerIdNotFoundError):
            ApplicationService.get_worker_details(params=status_params)
