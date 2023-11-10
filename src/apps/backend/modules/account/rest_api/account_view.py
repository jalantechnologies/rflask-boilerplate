from dataclasses import asdict

from flask import request, jsonify
from flask.views import MethodView
from flask.typing import ResponseReturnValue
from modules.account.types import CreateAccountParams
from modules.account.account_service import AccountService

class AccountView(MethodView):
  def post(self) -> ResponseReturnValue:
    request_data = request.get_json()
    account_params = CreateAccountParams(**request_data)
    account = AccountService.create_account(params=account_params)
    account_dict = asdict(account)
    return jsonify(account_dict), 201
