from flask import Blueprint

from modules.password_reset_token.rest_api.password_reset_token_view import PasswordResetTokenView


class PasswordResetTokenRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule(
            "/password-reset-tokens", view_func=PasswordResetTokenView.as_view("password_reset_token_view")
        )
        return blueprint
