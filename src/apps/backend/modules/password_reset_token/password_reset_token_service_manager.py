from flask import Blueprint

from modules.password_reset_token.rest_api.password_reset_token_rest_api_server import PasswordResetTokenRestApiServer


class PasswordResetTokenServiceManager:
    @staticmethod
    def create_rest_api_server() -> Blueprint:
        return PasswordResetTokenRestApiServer.create()
