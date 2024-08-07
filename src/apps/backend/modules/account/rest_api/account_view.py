from dataclasses import asdict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.account.account_service import AccountService
from modules.account.types import AccountSearchByIdParams, CreateAccountParams, ResetPasswordParams


class AccountView(MethodView):
    def post(self) -> ResponseReturnValue:
        request_data = request.get_json()
        account_params = CreateAccountParams(**request_data)
        account = AccountService.create_account(params=account_params)
        account_dict = asdict(account)
        return jsonify(account_dict), 201

    def get(self, id: str) -> ResponseReturnValue:
        account_params = AccountSearchByIdParams(id=id)
        account = AccountService.get_account_by_id(params=account_params)
        account_dict = asdict(account)
        return jsonify(account_dict), 200

    def patch(self, id: str) -> ResponseReturnValue:
        request_data = request.get_json()
        reset_account_params = ResetPasswordParams(account_id=id, **request_data)
        account = AccountService.reset_account_password(params=reset_account_params)
        account_dict = asdict(account)
        return jsonify(account_dict), 200
