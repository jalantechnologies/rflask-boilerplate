from modules.worker.types import WorkerPriority
from workers.base_worker import BaseWorker
from workers.worker_registry import register_worker


@register_worker
class TestDefaultWorker(BaseWorker):
    """
    A simple test worker to demonstrate the default-priority worker.
    """

    async def run(self, x: int, y: int) -> int:
        return x + y


@register_worker
class TestCriticalWorker(BaseWorker):
    """
    A simple test worker to demonstrate a critical-priority worker.
    """

    priority: WorkerPriority = WorkerPriority.CRITICAL

    async def run(self, x: int, y: int) -> int:
        return x + y
