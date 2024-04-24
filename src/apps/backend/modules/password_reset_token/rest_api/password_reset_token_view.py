from flask import request, jsonify
from flask.views import MethodView
from flask.typing import ResponseReturnValue

from dataclasses import asdict

from modules.communication.errors import ServiceError, ValidationError
from modules.password_reset_token.types import CreatePasswordResetTokenParams
from modules.account.errors import AccountNotFoundError
from modules.password_reset_token.password_reset_token_service import PasswordResetTokenService

class PasswordResetTokenView(MethodView):
    def post(self) -> ResponseReturnValue:
        try:
            request_data = request.get_json()
            password_reset_token_params = CreatePasswordResetTokenParams(**request_data)
            password_reset_token = PasswordResetTokenService.create_password_reset_token(params=password_reset_token_params)
            password_reset_token_dict = asdict(password_reset_token)
            return jsonify(password_reset_token_dict), 201
            
        except AccountNotFoundError as exc:
            return jsonify({
                "message": exc.message,
                "code": exc.code,
            }), 404
            
        except ValidationError as exc:
            return jsonify({
                "message": exc.message,
                "code": exc.code,
            }), 400
            
        except ServiceError as exc:
            return jsonify({
                "message": exc.message,
                "code": exc.code,
            }), 503
