from dotenv import load_dotenv
from flask import Flask, jsonify
from flask.typing import ResponseReturnValue
from flask_cors import CORS

from bin.blueprints import api_blueprint, img_assets_blueprint, react_blueprint
from modules.access_token.rest_api.access_token_rest_api_server import AccessTokenRestApiServer
from modules.account.rest_api.account_rest_api_server import AccountRestApiServer
from modules.config.config_manager import ConfigManager
from modules.error.custom_errors import AppError
from modules.logger.logger_manager import LoggerManager
from modules.password_reset_token.rest_api.password_reset_token_rest_api_server import PasswordResetTokenRestApiServer

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Mount deps
ConfigManager.mount_config()
LoggerManager.mount_logger()

# Register access token apis
access_token_blueprint = AccessTokenRestApiServer.create()
api_blueprint.register_blueprint(access_token_blueprint)

# Register password reset token apis
password_reset_token_blueprint = PasswordResetTokenRestApiServer.create()
api_blueprint.register_blueprint(password_reset_token_blueprint)

# Register accounts apis
account_blueprint = AccountRestApiServer.create()
api_blueprint.register_blueprint(account_blueprint)
app.register_blueprint(api_blueprint)

# Register frontend elements
app.register_blueprint(img_assets_blueprint)
app.register_blueprint(react_blueprint)


@app.errorhandler(AppError)
def handle_error(exc: AppError) -> ResponseReturnValue:
    return jsonify({"message": exc.message, "code": exc.code}), exc.http_code or 500
