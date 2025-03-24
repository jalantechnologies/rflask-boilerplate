from flask import Blueprint

from modules.authentication.rest_api.authentication_router import AuthenticationRouter


class AuthenticationRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        access_token_api_blueprint = Blueprint("access_token", __name__)
        return AuthenticationRouter.create_route(blueprint=access_token_api_blueprint)
