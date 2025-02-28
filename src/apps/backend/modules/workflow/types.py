from dataclasses import dataclass


@dataclass(frozen=True)
class SearchWorkflowByIdParams:
    id: str


@dataclass(frozen=True)
class QueueWorkflowParams:
    name: str
    arguments: list
    cron_schedule: str


@dataclass(frozen=True)
class WorkflowErrorCode:
    WORKFLOW_WITH_NAME_NOT_FOUND: str = "WORKER_ERR_01"
    WORKFLOW_WITH_ID_NOT_FOUND: str = "WORKER_ERR_02"
    WORKFLOW_START_ERROR: str = "WORKER_ERR_03"
    WORKFLOW_ALREADY_COMPLETED: str = "WORKER_ERR_04"
    WORKFLOW_ALREADY_CANCELLED: str = "WORKER_ERR_05"
    WORKFLOW_ALREADY_TERMINATED: str = "WORKER_ERR_06"
