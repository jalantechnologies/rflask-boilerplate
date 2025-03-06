from typing import Dict, Type

from temporalio import workflow

from modules.worker.types import WorkerPriority
from workers.base_worker import BaseWorker

# A global map storing worker metadata
WORKER_MAP: Dict[Type, WorkerPriority] = {}


def register_worker(cls: Type) -> Type:
    """
    Decorator to register a Temporal worker with additional metadata,
    enforcing that the worker inherits from BaseWorker and has a run() method.
    """
    if not issubclass(cls, BaseWorker):
        raise TypeError(f"Worker '{cls.__name__}' must inherit from BaseWorker")

    # Ensure there's a run() method to wrap.
    if not hasattr(cls, "run"):
        raise ValueError(f"Worker '{cls.__name__}' must define a 'run' method")

    # Wrap the run() method so Temporal recognizes it as the worker entry point.
    wrapped_run = workflow.run(cls.run)
    setattr(cls, "run", wrapped_run)

    # Decorate the class itself as a worker definition.
    cls = workflow.defn(cls)

    # Register in the global map, storing the assigned priority.
    WORKER_MAP[cls] = cls.priority

    return cls


# Import all workers to be registered below
import workers.dummy_workers  # noqa: F401
