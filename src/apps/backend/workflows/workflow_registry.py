from typing import Any, Dict, Type

from temporalio import workflow

from workflows.base_workflow import BaseWorkflow

# A global map storing workflow metadata
WORKFLOW_MAP: Dict[str, Dict[str, Any]] = {}


def register_workflow(cls: Type) -> Type:
    """
    Decorator to register a Temporal workflow with additional metadata,
    enforcing that the workflow inherits from BaseWorker and has a run() method.
    """
    if not issubclass(cls, BaseWorkflow):
        raise TypeError(f"Workflow '{cls.__name__}' must inherit from BaseWorker")

    # Ensure there's a run() method to wrap.
    if not hasattr(cls, "run"):
        raise ValueError(f"Workflow '{cls.__name__}' must define a 'run' method")

    # Wrap the run() method so Temporal recognizes it as the workflow entry point.
    wrapped_run = workflow.run(cls.run)
    setattr(cls, "run", wrapped_run)

    # Decorate the class itself as a workflow definition.
    cls = workflow.defn(cls)

    # Register in the global map, storing the assigned priority.
    WORKFLOW_MAP[cls.__name__] = {"priority": cls.priority, "class": cls}

    return cls


# Import all workflows to be registered below
import workflows.dummy_workflows  # noqa: F401
