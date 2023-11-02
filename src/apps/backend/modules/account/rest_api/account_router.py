from flask import Blueprint
from modules.account.rest_api.account_view import AccountView


class AccountRouter:
  @staticmethod
  def create_route(*, blueprint: Blueprint) -> Blueprint:
    blueprint.add_url_rule("/account", view_func=AccountView.as_view("account_view"))
    return blueprint
