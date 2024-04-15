from flask import Blueprint
from modules.access_token.rest_api.access_token_rest_api_server import AccessTokenRestApiServer

class AccessTokenServiceManager:
    @staticmethod
    def create_rest_api_server() -> Blueprint:
        return AccessTokenRestApiServer.create()
