from dataclasses import dataclass


@dataclass(frozen=True)
class SearchWorkflowByIdParams:
    id: str


@dataclass(frozen=True)
class SearchWorkflowByNameParams:
    name: str


@dataclass(frozen=True)
class QueueWorkflowParams:
    workflow_name: str
    workflow_params: list


@dataclass(frozen=True)
class WorkerErrorCode:
    WORKFLOW_WITH_NAME_NOT_FOUND: str = "WORKER_ERR_01"
    WORKFLOW_WITH_ID_NOT_FOUND: str = "WORKER_ERR_02"
    WORKFLOW_START_ERROR: str = "WORKER_ERR_03"
