from dataclasses import asdict

from flask import request, jsonify
from flask.views import MethodView
from flask.typing import ResponseReturnValue

from modules.account.types import AccountSearchByIdParams, CreateAccountParams, ResetPasswordParams
from modules.account.account_service import AccountService
from modules.account.errors import AccountNotFoundError, AccountWithUserNameExistsError

class AccountView(MethodView):
  def post(self) -> ResponseReturnValue:
    try:
      request_data = request.get_json()
      account_params = CreateAccountParams(**request_data)
      account = AccountService.create_account(params=account_params)
      account_dict = asdict(account)
      return jsonify(account_dict), 201
    except AccountWithUserNameExistsError as exc:
      return jsonify({
        "message": exc.message,
        "code": exc.code,
      }), 400
      
  def get(self, id) -> ResponseReturnValue:
    try:
      account_params = AccountSearchByIdParams(id=id)
      account = AccountService.get_account_by_id(params=account_params)
      account_dict = asdict(account)
      return jsonify(account_dict), 200
    except AccountNotFoundError as exc:
      return jsonify({
        "message": exc.message,
        "code": exc.code,
      }), 400
      
  def patch(self, id) -> ResponseReturnValue:
    try:
      request_data = request.get_json()
      reset_account_params = ResetPasswordParams(account_id=id, **request_data)
      account = AccountService.reset_account_password(params=reset_account_params)
      account_dict = asdict(account)
      return jsonify(account_dict), 200
    
    except AccountNotFoundError as exc:
      return jsonify({
        "message": exc.message,
        "code": exc.code,
      }), 400
