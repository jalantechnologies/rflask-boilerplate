import time

import pytest
from temporalio.client import WorkflowExecutionStatus
from tests.modules.worker.base_test_worker import BaseTestWorker

from modules.worker.errors import (
    WorkerClassInvalidError,
    WorkerClassNotRegisteredError,
    WorkerIdNotFoundError,
)
from modules.worker.types import RunWorkerParams, SearchWorkerByIdParams, WorkerPriority
from modules.worker.worker_service import WorkerService
from workers.base_worker import BaseWorker
from workers.dummy_workers import TestDefaultWorker


class TestWorkerService(BaseTestWorker):
    def test_get_all_workers(self) -> None:
        workers_list = WorkerService.get_all_workers()
        assert {
            "name": TestDefaultWorker,
            "priority": WorkerPriority.DEFAULT,
        } in workers_list

    def test_queue_and_get_details_worker(self) -> None:
        queue_params = RunWorkerParams(
            TestDefaultWorker, arguments=[10, 5], cron_schedule=""
        )
        worker_id = WorkerService.run_worker(params=queue_params)
        assert worker_id

        time.sleep(1)

        details_params = SearchWorkerByIdParams(id=worker_id)
        data = WorkerService.get_worker_details(params=details_params)
        assert data["worker_id"] == worker_id
        assert int(data["runs"][0]["result"]) == 15
        assert data["status"] == WorkflowExecutionStatus.COMPLETED

    def test_queue_worker_with_invalid_class(self) -> None:
        class InvalidWorker: ...

        run_params = RunWorkerParams(InvalidWorker, arguments=[10, 5], cron_schedule="")
        with pytest.raises(WorkerClassInvalidError):
            WorkerService.run_worker(params=run_params)

    def test_queue_worker_with_invalid_name(self) -> None:
        class NonExistentWorker(BaseWorker):
            async def run(self) -> None: ...

        run_params = RunWorkerParams(
            NonExistentWorker, arguments=[10, 5], cron_schedule=""
        )
        with pytest.raises(WorkerClassNotRegisteredError):
            WorkerService.run_worker(params=run_params)

    def test_get_details_with_invalid_worker_id(self) -> None:
        status_params = SearchWorkerByIdParams(id="non_existent")
        with pytest.raises(WorkerIdNotFoundError):
            WorkerService.get_worker_details(params=status_params)
