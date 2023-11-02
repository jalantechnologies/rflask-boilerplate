from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify, Response
from flask_cors import CORS
from bin.blueprints import api_blueprint, img_assets_blueprint, react_blueprint
from modules.config.config_manager import ConfigManager
from modules.account.account_service_manager import AccountServiceManager
from modules.error.app_error import AppError
from modules.logger.logger_manager import LoggerManager

app = Flask(__name__)
cors = CORS(app)

ConfigManager.mount_config()
LoggerManager.mount_logger()


# Register account apps
account_blueprint = AccountServiceManager.create_rest_api_server()
api_blueprint.register_blueprint(account_blueprint)
app.register_blueprint(api_blueprint)

# Register experience apps
app.register_blueprint(img_assets_blueprint)
app.register_blueprint(react_blueprint)


@app.errorhandler(Exception)
def custom_error_handler(error) -> tuple[Response, int | None]:
  if isinstance(error, AppError):
    return jsonify(error.message), error.status_code

  code = error.code if isinstance(error, HTTPException) else 500
  return jsonify(error=str(error)), code
