from modules.access_token.rest_api.access_token_view import AccessTokenView
from flask import Blueprint


class AccessTokenRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule("/access-tokens", view_func=AccessTokenView.as_view("access_token_view"))
        return blueprint
