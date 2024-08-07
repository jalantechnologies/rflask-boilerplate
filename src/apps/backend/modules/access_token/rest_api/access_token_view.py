from dataclasses import asdict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.access_token.access_token_service import AccessTokenService
from modules.access_token.types import CreateAccessTokenParams


class AccessTokenView(MethodView):
    def post(self) -> ResponseReturnValue:
        request_data = request.get_json()
        access_token_params = CreateAccessTokenParams(**request_data)
        access_token = AccessTokenService.create_access_token(params=access_token_params)
        access_token_dict = asdict(access_token)
        return jsonify(access_token_dict), 201
