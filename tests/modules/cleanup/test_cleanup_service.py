from unittest.mock import ANY, MagicMock, patch

from modules.cleanup.cleanup_service import CleanupService
from modules.cleanup.types import CreateAccountDeletionRequestParams

from tests.modules.cleanup.base_test_cleanup import BaseTestCleanup


class TestCleanupService(BaseTestCleanup):
    @patch("modules.cleanup.internal.cleanup_manager.CleanupManager.register_hook")
    def test_register(self, mock_register_hook):
        func = MagicMock(
            __name__="mock_func",
            __module__="mock_module",
            __qualname__="MockClass.mock_func",
        )
        decorator = CleanupService.register()
        decorated_func = decorator(func)

        mock_register_hook.assert_called_once_with(
            func=func, module_name="mock_module", class_name="MockClass", main=False
        )
        self.assertEqual(decorated_func, func)

    @patch("modules.cleanup.internal.cleanup_manager.CleanupManager.push_hooks")
    def test_push_hooks(self, mock_push_hooks):
        CleanupService.push_hooks()
        mock_push_hooks.assert_called_once()

    @patch(
        "modules.account.account_service.AccountService.get_account_by_id",
        return_value=True,
    )
    @patch("modules.account.account_service.AccountService.deactivate_account")
    @patch(
        "modules.cleanup.internal.cleanup_manager.CleanupManager.queue_account_deletion"
    )
    def test_queue_account_deletion(
        self, mock_queue_account_deletion, mock_deactivate_account, mock_get_account
    ):
        CleanupService.queue_account_deletion(params=self.params)

        mock_get_account.assert_called_once_with(params=self.params)
        mock_deactivate_account.assert_called_once_with(params=self.params)
        mock_queue_account_deletion.assert_called_once_with(
            params=CreateAccountDeletionRequestParams(
                account_id=self.params.id, requested_at=ANY
            )
        )

    @patch(
        "modules.account.account_service.AccountService.get_account_by_id",
        return_value=None,
    )
    def test_queue_account_deletion_fails_if_account_not_found(self, mock_get_account):
        with self.assertRaises(Exception) as context:
            CleanupService.queue_account_deletion(params=self.params)

        self.assertTrue("Account not found" in str(context.exception))
        mock_get_account.assert_called_once_with(params=self.params)
