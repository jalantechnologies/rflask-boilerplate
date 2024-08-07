from flask import Blueprint

from modules.access_token.rest_api.access_token_router import AccessTokenRouter


class AccessTokenRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        access_token_api_blueprint = Blueprint("access_token", __name__)
        return AccessTokenRouter.create_route(blueprint=access_token_api_blueprint)
