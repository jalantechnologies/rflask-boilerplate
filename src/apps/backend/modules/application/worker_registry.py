from typing import Type

from temporalio import workflow

from modules.application.application_service import ApplicationService
from modules.application.types import BaseWorker


def register_worker(cls: Type[BaseWorker]) -> Type[BaseWorker]:
    """
    Decorator to register a Temporal application with additional metadata,
    enforcing that the application inherits from BaseWorker and has a run() method.
    """
    # Wrap the run() method so Temporal recognizes it as the application entry point.
    wrapped_run = workflow.run(cls.run)
    setattr(cls, "run", wrapped_run)

    # Decorate the class itself as a application definition.
    cls = workflow.defn(cls)

    # Register in the global map, storing the assigned priority.
    ApplicationService.register_worker(cls)

    return cls
