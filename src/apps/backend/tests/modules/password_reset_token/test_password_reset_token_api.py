import json
from unittest import mock

from modules.account.account_service import AccountService
from modules.account.errors import AccountBadRequestError, AccountNotFoundError
from modules.account.types import CreateAccountParams
from modules.communication.email_service import EmailService
from modules.password_reset_token.errors import PasswordResetTokenNotFoundError
from modules.password_reset_token.internal.password_reset_token_util import PasswordResetTokenUtil
from modules.password_reset_token.internal.password_reset_token_writer import PasswordResetTokenWriter
from modules.password_reset_token.password_reset_token_service import PasswordResetTokenService
from modules.password_reset_token.types import CreatePasswordResetTokenParams
from server import app
from tests.modules.password_reset_token.base_test_password_reset_token import BaseTestPasswordResetToken

ACCOUNT_API_URL = "http://127.0.0.1:8080/api/accounts"
PASSWORD_RESET_TOKEN_URL = "http://127.0.0.1:8080/api/password-reset-tokens"
HEADERS = {"Content-Type": "application/json"}


class TestAccountPasswordReset(BaseTestPasswordResetToken):

    # POST /password-reset-tokens tests
    @mock.patch.object(EmailService, "send_email")
    def test_create_password_reset_token(self, mock_send_email) -> None:
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        reset_password_params = {"username": account.username}

        with app.test_client() as client:
            response = client.post(PASSWORD_RESET_TOKEN_URL, headers=HEADERS, data=json.dumps(reset_password_params))

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.json)
            self.assertIn("id", response.json)
            self.assertIn("account", response.json)
            self.assertIn("token", response.json)
            self.assertFalse(response.json["is_used"])
            self.assertTrue(mock_send_email.called)
            self.assertIn("password_reset_link", mock_send_email.call_args.kwargs["params"].template_data)
            self.assertEqual(response.json["account"], account.id)

    @mock.patch.object(EmailService, "send_email")
    def test_create_password_reset_token_account_not_found(self, mock_send_email):
        username = "nonexistent_username@example.com"
        reset_password_params = {"username": username}

        with app.test_client() as client:
            response = client.post(PASSWORD_RESET_TOKEN_URL, headers=HEADERS, data=json.dumps(reset_password_params))

            self.assertEqual(response.status_code, 404)
            self.assertIn("message", response.json)
            self.assertEqual(
                response.json["message"], AccountNotFoundError(f"Account with username:: {username}, not found").message
            )
            self.assertFalse(mock_send_email.called)

    # PATCH /account/:account_id tests
    @mock.patch.object(EmailService, "send_email")
    def test_reset_account_password(self, mock_send_email):
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        token = PasswordResetTokenUtil.generate_password_reset_token()
        PasswordResetTokenWriter.create_password_reset_token(account.id, token)
        PasswordResetTokenService.send_password_reset_email(account.id, account.first_name, account.username, token)

        new_password = "new_password"

        reset_password_params = {"new_password": new_password, "token": token}

        with app.test_client() as client:
            response = client.patch(
                f"{ACCOUNT_API_URL}/{account.id}", headers=HEADERS, data=json.dumps(reset_password_params)
            )

            self.assertEqual(response.status_code, 200)
            self.assertIn("id", response.json)
            self.assertIn("username", response.json)
            self.assertEqual(response.json["id"], account.id)
            self.assertEqual(response.json["username"], account.username)

            # Check if password reset token is marked as used.
            updated_password_reset_token = PasswordResetTokenService.get_password_reset_token_by_account_id(account.id)
            self.assertTrue(updated_password_reset_token.is_used)
            self.assertTrue(mock_send_email.called)

    @mock.patch.object(EmailService, "send_email")
    def test_reset_account_password_account_not_found(self, mock_send_email):
        account_id = "661e42ec98423703a299a899"
        new_password = "new_password"
        token = "token"

        reset_password_params = {"new_password": new_password, "token": token}

        with app.test_client() as client:
            response = client.patch(
                f"{ACCOUNT_API_URL}/{account_id}", headers=HEADERS, data=json.dumps(reset_password_params)
            )

            print(response.json)

            self.assertEqual(response.status_code, 404)
            self.assertIn("message", response.json)
            self.assertEqual(
                response.json["message"], AccountNotFoundError(f"Account with id:: {account_id}, not found").message
            )
            self.assertFalse(mock_send_email.called)

    @mock.patch.object(EmailService, "send_email")
    def test_reset_account_password_token_not_found(self, mock_send_email):
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        new_password = "new_password"
        token = "token"

        reset_password_params = {"new_password": new_password, "token": token}

        with app.test_client() as client:
            response = client.patch(
                f"{ACCOUNT_API_URL}/{account.id}", headers=HEADERS, data=json.dumps(reset_password_params)
            )

            self.assertEqual(response.status_code, 404)
            self.assertIn("message", response.json)
            self.assertEqual(response.json["message"], PasswordResetTokenNotFoundError().message)
            self.assertFalse(mock_send_email.called)

    @mock.patch.object(EmailService, "send_email")
    def test_reset_account_password_token_already_used(self, mock_send_email):
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        password_reset_token = PasswordResetTokenService.create_password_reset_token(
            params=CreatePasswordResetTokenParams(username=account.username)
        )

        PasswordResetTokenService.set_password_reset_token_as_used_by_id(password_reset_token.id)

        new_password = "new_password"

        reset_password_params = {"new_password": new_password, "token": password_reset_token.token}

        with app.test_client() as client:
            response = client.patch(
                f"{ACCOUNT_API_URL}/{account.id}", headers=HEADERS, data=json.dumps(reset_password_params)
            )

            self.assertEqual(response.status_code, 400)
            self.assertIn("message", response.json)
            self.assertEqual(
                response.json["message"],
                AccountBadRequestError(
                    f"Password reset is already used for accountId {account.id}. Please retry with new link"
                ).message,
            )
            self.assertTrue(mock_send_email.called)

    @mock.patch.object(EmailService, "send_email")
    def test_reset_account_password_invalid_token(self, mock_send_email):
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        PasswordResetTokenService.create_password_reset_token(
            params=CreatePasswordResetTokenParams(username=account.username)
        )

        new_password = "new_password"

        reset_password_params = {"new_password": new_password, "token": "invalid_token"}

        with app.test_client() as client:
            response = client.patch(
                f"{ACCOUNT_API_URL}/{account.id}", headers=HEADERS, data=json.dumps(reset_password_params)
            )

            self.assertEqual(response.status_code, 400)
            self.assertIn("message", response.json)
            self.assertEqual(
                response.json["message"],
                AccountBadRequestError(
                    f"Password reset link is invalid for accountId {account.id}. Please retry with new link."
                ).message,
            )
            self.assertTrue(mock_send_email.called)

    @mock.patch.object(EmailService, "send_email")
    @mock.patch.object(PasswordResetTokenUtil, "is_token_expired")
    def test_reset_account_password_expired_token(self, mock_is_token_expired, mock_send_email):
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        password_reset_token = PasswordResetTokenService.create_password_reset_token(
            params=CreatePasswordResetTokenParams(username=account.username)
        )

        mock_is_token_expired.return_value = True

        new_password = "new_password"

        reset_password_params = {"new_password": new_password, "token": password_reset_token.token}

        with app.test_client() as client:
            response = client.patch(
                f"{ACCOUNT_API_URL}/{account.id}", headers=HEADERS, data=json.dumps(reset_password_params)
            )

            self.assertEqual(response.status_code, 400)
            self.assertIn("message", response.json)
            self.assertEqual(
                response.json["message"],
                AccountBadRequestError(
                    f"Password reset link is expired for accountId {account.id}. Please retry with new link"
                ).message,
            )
            self.assertTrue(mock_send_email.called)
