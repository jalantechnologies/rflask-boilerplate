from dataclasses import asdict

from modules.access_token.access_token_service import AccessTokenService
from modules.access_token.types import CreateAccessTokenParams
from flask import request, jsonify
from flask.views import MethodView
from flask.typing import ResponseReturnValue


class AccessTokenView(MethodView):
    def post(self) -> ResponseReturnValue:
        request_data = request.get_json()
        access_token_params = CreateAccessTokenParams(**request_data)
        access_token = AccessTokenService.create_access_token(params=access_token_params)
        access_token_dict = asdict(access_token)
        return jsonify(access_token_dict), 201
