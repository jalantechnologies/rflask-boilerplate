from flask import Flask
from flask_cors import CORS
from bin.blueprints import api_blueprint, img_assets_blueprint, react_blueprint
from modules.config.config_manager import ConfigManager
from modules.access_token.access_token_service_manager import AccessTokenServiceManager
from modules.password_reset_token.password_reset_token_service_manager import PasswordResetTokenServiceManager
from modules.account.account_service_manager import AccountServiceManager
from modules.logger.logger_manager import LoggerManager

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Mount deps
ConfigManager.mount_config()
LoggerManager.mount_logger()

# Register access token apis
access_token_blueprint = AccessTokenServiceManager.create_rest_api_server()
api_blueprint.register_blueprint(access_token_blueprint)

# Register password reset token apis
password_reset_token_blueprint = PasswordResetTokenServiceManager.create_rest_api_server()
api_blueprint.register_blueprint(password_reset_token_blueprint)

# Register accounts apis
account_blueprint = AccountServiceManager.create_rest_api_server()
api_blueprint.register_blueprint(account_blueprint)
app.register_blueprint(api_blueprint)

# Register frontend elements
app.register_blueprint(img_assets_blueprint)
app.register_blueprint(react_blueprint)
