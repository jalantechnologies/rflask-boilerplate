from flask import Blueprint
from modules.account.rest_api.account_rest_api_server import AccountRestApiServer


class AccountServiceManager:
  @staticmethod
  def create_rest_api_server() -> Blueprint:
    return AccountRestApiServer.create()
