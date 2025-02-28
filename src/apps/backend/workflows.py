import asyncio
from typing import Any, Callable, Dict, Type

from dotenv import load_dotenv
from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker

with workflow.unsafe.imports_passed_through():
    from modules.config.config_manager import ConfigManager
    from modules.config.config_service import ConfigService
    from modules.logger.logger import Logger
    from modules.logger.logger_manager import LoggerManager

# Global registry for workflows
WORKFLOW_MAP: Dict[str, Dict[str, Any]] = {}


def register_temporal_workflow(
    priority: str = "default",
) -> Callable:
    """
    Decorator to register a Temporal workflow with additional metadata.
    """

    def decorator(cls: Type) -> Type:
        if hasattr(cls, "run"):
            cls.run = workflow.run(
                cls.run
            )  # Wrap the run method as a Temporal workflow

        else:
            raise ValueError(f"Class '{cls.__name__}' does not have a 'run' method")

        cls = workflow.defn(cls)  # Wrap the class as a Temporal workflow

        # Register the workflow in the global map
        WORKFLOW_MAP[cls.__name__] = {
            "priority": priority,
            "class": cls,
        }

        return cls

    return decorator


# Just for demonstration; in practice this would be done inside a module
@register_temporal_workflow()
class TestDefaultWorkflow:
    """
    A simple test workflow to demonstrate the Temporal workflow decorator.

    This workflow adds two numbers together.
    """

    async def run(self, x: int, y: int) -> int:
        return x + y


# Just for demonstration; in practice this would be done inside a module
@register_temporal_workflow(
    priority="critical",
)
class TestCriticalWorkflow:
    """
    A simple test workflow to demonstrate the Temporal workflow decorator.

    This workflow adds two numbers together.
    """

    async def run(self, x: int, y: int) -> int:
        return x + y


async def main() -> None:
    load_dotenv()

    # Mount configuration and logger
    ConfigManager.mount_config()
    LoggerManager.mount_logger()

    temporal_server = ConfigService.get_string("TEMPORAL_SERVER_ADDRESS")
    client = await Client.connect(temporal_server)

    default_queue = ConfigService.get_string("TEMPORAL_DEFAULT_TASK_QUEUE")
    critical_queue = ConfigService.get_string("TEMPORAL_CRITICAL_TASK_QUEUE")

    Logger.info(
        message=f"Starting workers on queues: Default='{default_queue}', Critical='{critical_queue}'"
    )

    # Create workers for each priority level
    workflows_default = [
        wf["class"] for wf in WORKFLOW_MAP.values() if wf["priority"] == "default"
    ]
    workflows_critical = [
        wf["class"] for wf in WORKFLOW_MAP.values() if wf["priority"] == "critical"
    ]

    worker_default = Worker(
        client, task_queue=default_queue, workflows=workflows_default
    )
    worker_critical = Worker(
        client, task_queue=critical_queue, workflows=workflows_critical
    )

    # Run both workers concurrently
    await asyncio.gather(worker_default.run(), worker_critical.run())


if __name__ == "__main__":
    asyncio.run(main())
