from flask import request, Response, jsonify
from flask.views import MethodView
from dataclasses import asdict

from modules.account.types import CreateAccountParams
from modules.account.account_service import AccountService
from modules.logger.logger import Logger


class AccountView(MethodView):
  def post(self) -> Response:
    request_data = request.get_json()
    Logger.info(message=f"Requested data :: {request_data}")
    account_params = CreateAccountParams(**request_data)
    account = AccountService.create_account(params=account_params)
    account_dict = asdict(account)
    response = jsonify(account_dict)
    response.status_code = 201
    return response
