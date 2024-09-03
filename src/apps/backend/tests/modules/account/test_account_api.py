import json
from unittest import mock

from modules.communication.sms_service import SMSService
from modules.otp.types import OtpErrorCode
from modules.account.account_service import AccountService
from modules.account.types import AccountErrorCode, CreateAccountByPhoneNumberParams, CreateAccountByUsernameAndPasswordParams, PhoneNumber
from server import app
from tests.modules.account.base_test_account import BaseTestAccount


class TestAccountApi(BaseTestAccount):
    def test_create_account_by_username_and_password(self) -> None:
        payload = json.dumps(
            {"first_name": "first_name", "last_name": "last_name", "password": "password", "username": "username"}
        )

        with app.test_client() as client:
            response = client.post(
                "http://127.0.0.1:8080/api/accounts", headers={"Content-Type": "application/json"}, data=payload
            )
            assert response.status_code == 201
            assert response.json, f"No response from API with status code:: {response.status}"
            assert response.json.get("username") == "username"

    def test_create_account_with_existing_user(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )
        with app.test_client() as client:
            response = client.post(
                "http://127.0.0.1:8080/api/accounts",
                headers={"Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "first_name": "first_name",
                        "last_name": "last_name",
                        "password": "password",
                        "username": account.username,
                    }
                ),
            )
        assert response.status_code == 409
        assert response.json
        assert response.json.get("code") == AccountErrorCode.USERNAME_ALREADY_EXISTS

    @mock.patch.object(SMSService, "send_sms")
    def test_create_account_by_phone_number_and_send_otp(self, mock_send_sms) -> None:
        payload = json.dumps({"phone_number": {"country_code": "+91", "phone_number": "9999999999"}})
        
        with app.test_client() as client:
            response = client.post(
                "http://127.0.0.1:8080/api/accounts", headers={"Content-Type": "application/json"}, data=payload
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json.get("phone_number"), {"country_code": "+91", "phone_number": "9999999999"})
            self.assertIn("id", response.json)
            self.assertTrue(mock_send_sms.called)
            self.assertEqual(mock_send_sms.call_args.kwargs['params'].recipient_phone, PhoneNumber(country_code="+91", phone_number="9999999999"))
            self.assertIn("is your One Time Password (OTP) for verification.", mock_send_sms.call_args.kwargs["params"].message_body)
    
    @mock.patch.object(SMSService, "send_sms")
    def test_get_account_with_existing_phone_number_and_send_otp(self, mock_send_sms) -> None:
        AccountService.get_or_create_account_by_phone_number(params=CreateAccountByPhoneNumberParams(phone_number={"country_code": "+91", "phone_number": "9999999999"}))
        with app.test_client() as client:
            response = client.post(
                "http://127.0.0.1:8080/api/accounts", headers={"Content-Type": "application/json"}, data=json.dumps(
                    {"phone_number": {"country_code": "+91", "phone_number": "9999999999"}}
                ),
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("phone_number"), {"country_code": "+91", "phone_number": "9999999999"})
        self.assertIn("id", response.json)
        self.assertTrue(mock_send_sms.called)
        self.assertEqual(mock_send_sms.call_args.kwargs['params'].recipient_phone, PhoneNumber(country_code="+91", phone_number="9999999999"))
        self.assertIn("is your One Time Password (OTP) for verification.", mock_send_sms.call_args.kwargs["params"].message_body)
        
    @mock.patch.object(SMSService, "send_sms")
    def test_get_or_create_account_with_invalid_phone_number(self, mock_send_sms) -> None:
        payload = json.dumps({"phone_number": {"country_code": "+91", "phone_number": "999999999"}})
        with app.test_client() as client:
            response = client.post(
                "http://127.0.0.1:8080/api/accounts", headers={"Content-Type": "application/json"}, data=payload
            )
            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.json)
            self.assertEqual(response.json.get("code"), OtpErrorCode.REQUEST_FAILED)
            self.assertEqual(response.json.get("message"), "Please provide a valid phone number.")
            self.assertFalse(mock_send_sms.called)
