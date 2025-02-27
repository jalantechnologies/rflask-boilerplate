from dataclasses import dataclass


@dataclass(frozen=True)
class SearchWorkflowByIdParams:
    id: str


@dataclass(frozen=True)
class QueueWorkflowParams:
    name: str
    arguments: list
    priority: str
    cron_schedule: str


@dataclass(frozen=True)
class WorkflowErrorCode:
    WORKFLOW_WITH_NAME_NOT_FOUND: str = "WORKER_ERR_01"
    WORKFLOW_WITH_ID_NOT_FOUND: str = "WORKER_ERR_02"
    WORKFLOW_START_ERROR: str = "WORKER_ERR_03"
