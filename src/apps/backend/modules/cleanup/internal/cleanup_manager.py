import importlib
from typing import Callable, List

from modules.account.types import SearchAccountByIdParams
from modules.cleanup.internal.account_deletion_request_writer import AccountDeletionRequestWriter
from modules.cleanup.internal.cleanup_module_writer import CleanupModuleWriter
from modules.cleanup.types import (
    AccountDeletionRequest,
    CleanupModule,
    CreateAccountDeletionRequestParams,
    CreateCleanupModuleParams,
)
from modules.logger.logger import Logger


class CleanupManager:
    HOOKS: List[CreateCleanupModuleParams] = []

    @staticmethod
    def register_hook(func: Callable, module_name: str, class_name: str, main: bool = False) -> None:
        """Register a cleanup hook."""
        params = CreateCleanupModuleParams(
            module_name=module_name, class_name=class_name, function_name=func.__name__, main=main
        )
        CleanupManager.HOOKS.append(params)

    @staticmethod
    def push_hooks() -> None:
        """Push all registered hooks to the database."""
        CleanupModuleWriter.clear_cleanup_modules()

        for hook in CleanupManager.HOOKS:
            CleanupModuleWriter.add_cleanup_module(params=hook)

            if hook.main:
                Logger.info(message=f"Registered main hook: {hook.function_name}")

            Logger.info(message=f"Registered cleanup hook: {hook.function_name}")

        CleanupManager.HOOKS = []

    @staticmethod
    def queue_account_deletion(params: CreateAccountDeletionRequestParams) -> None:
        """Queue cleanup operation to be handled by the worker thread."""
        AccountDeletionRequestWriter.create_account_deletion_request(params=params)

    @staticmethod
    def execute_hook(*, cleanup_module: CleanupModule, account_deletion_request: AccountDeletionRequest) -> None:
        """Execute a cleanup hook."""
        module = importlib.import_module(cleanup_module.module_name)
        cleanup_class = getattr(module, cleanup_module.class_name)
        cleanup_function = cleanup_class.__dict__[cleanup_module.function_name]

        params = SearchAccountByIdParams(id=account_deletion_request.account_id)
        cleanup_function(params=params)
