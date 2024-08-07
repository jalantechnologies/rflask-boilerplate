from flask import request, jsonify
from flask.views import MethodView
from flask.typing import ResponseReturnValue

from dataclasses import asdict

from modules.password_reset_token.types import CreatePasswordResetTokenParams
from modules.password_reset_token.password_reset_token_service import PasswordResetTokenService


class PasswordResetTokenView(MethodView):
    def post(self) -> ResponseReturnValue:
        request_data = request.get_json()
        password_reset_token_params = CreatePasswordResetTokenParams(**request_data)
        password_reset_token = PasswordResetTokenService.create_password_reset_token(params=password_reset_token_params)
        password_reset_token_dict = asdict(password_reset_token)
        return jsonify(password_reset_token_dict), 201
