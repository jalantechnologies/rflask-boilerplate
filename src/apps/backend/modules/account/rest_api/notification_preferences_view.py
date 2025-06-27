from dataclasses import asdict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.account.account_service import AccountService
from modules.account.types import AccountSearchByIdParams, NotificationPreferences, UpdateNotificationPreferencesParams
from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware


class NotificationPreferencesView(MethodView):
    @access_auth_middleware
    def get(self, account_id: str) -> ResponseReturnValue:
        account = AccountService.get_account_by_id(params=AccountSearchByIdParams(id=account_id))

        preferences = account.notification_preferences or NotificationPreferences()
        return jsonify(asdict(preferences)), 200

    @access_auth_middleware
    def put(self, account_id: str) -> ResponseReturnValue:
        request_data = request.get_json()

        update_params = UpdateNotificationPreferencesParams(
            account_id=account_id,
            email_enabled=request_data.get("email_enabled", True),
            sms_enabled=request_data.get("sms_enabled", True),
            push_enabled=request_data.get("push_enabled", False),
        )

        updated_account = AccountService.update_notification_preferences(params=update_params)

        preferences = updated_account.notification_preferences or NotificationPreferences()
        return jsonify(asdict(preferences)), 200
