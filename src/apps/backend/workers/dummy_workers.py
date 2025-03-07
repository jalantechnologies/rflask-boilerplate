from modules.application.types import WorkerPriority
from workers.base_worker import BaseWorker
from workers.worker_registry import register_worker


@register_worker
class TestDefaultWorker(BaseWorker):
    """
    A simple test application to demonstrate the default-priority application.
    """

    async def run(self, x: int, y: int) -> int:
        return x + y


@register_worker
class TestCriticalWorker(BaseWorker):
    """
    A simple test application to demonstrate a critical-priority application.
    """

    priority: WorkerPriority = WorkerPriority.CRITICAL

    async def run(self, x: int, y: int) -> int:
        return x + y
