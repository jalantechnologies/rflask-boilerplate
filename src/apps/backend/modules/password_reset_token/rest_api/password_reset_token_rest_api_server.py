from flask import Blueprint

from modules.password_reset_token.rest_api.password_reset_token_router import PasswordResetTokenRouter
from modules.password_reset_token.internal.store.password_reset_token_repository import PasswordResetTokenRepository

class PasswordResetTokenRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        PasswordResetTokenRepository.create_db_connection()
        password_reset_token_api_blueprint = Blueprint("password_reset_token", __name__)
        return PasswordResetTokenRouter.create_route(blueprint=password_reset_token_api_blueprint)
