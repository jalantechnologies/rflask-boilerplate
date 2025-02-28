from typing import Any, Callable, Dict, Type

from temporalio import workflow

# Global registry for workflows
WORKFLOW_MAP: Dict[str, Dict[str, Any]] = {}


def register_temporal_workflow(priority: str = "default") -> Callable:
    """
    Decorator to register a Temporal workflow with additional metadata.
    """

    def decorator(cls: Type) -> Type:
        if hasattr(cls, "run"):
            cls.run = workflow.run(cls.run)  # Wrap the run method as a Temporal workflow runner method

        else:
            raise ValueError(f"Class '{cls.__name__}' does not have a 'run' method")

        cls = workflow.defn(cls)  # Wrap the class as a Temporal workflow

        # Register the workflow in the global map
        WORKFLOW_MAP[cls.__name__] = {"priority": priority, "class": cls}

        return cls

    return decorator


# Import all workflows to be registered below
import workflows.dummy_workflows  # noqa: F401
