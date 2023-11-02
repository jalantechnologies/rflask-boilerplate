from flask import request, Response, jsonify
from flask.views import MethodView
from dataclasses import asdict

from modules.account.types import CreateAccountParams
from modules.account.account_service import AccountService


class AccountView(MethodView):
  def post(self) -> Response:
    request_data = request.get_json()
    account_params = CreateAccountParams(**request_data)
    account = AccountService.create_account(params=account_params)
    print(account)
    return Response({
      "username": account.username
    }, status=201)

  def get(self):
    return Response("ok", status=200)
