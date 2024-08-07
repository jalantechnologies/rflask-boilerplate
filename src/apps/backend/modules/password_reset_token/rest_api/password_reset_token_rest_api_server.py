from flask import Blueprint

from modules.password_reset_token.rest_api.password_reset_token_router import PasswordResetTokenRouter


class PasswordResetTokenRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        password_reset_token_api_blueprint = Blueprint("password_reset_token", __name__)
        return PasswordResetTokenRouter.create_route(blueprint=password_reset_token_api_blueprint)
