from flask import Flask
from flask_cors import CORS
from bin.blueprints import api_blueprint, img_assets_blueprint, react_blueprint
from modules.config.config_manager import ConfigManager
from modules.access_token.rest_api.access_token_rest_api_server import AccessTokenRestApiServer
from modules.account.rest_api.account_rest_api_server import AccountRestApiServer
from modules.logger.logger_manager import LoggerManager

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Mount deps
ConfigManager.mount_config()
LoggerManager.mount_logger()

# Register access token apis
access_token_blueprint = AccessTokenRestApiServer.create()
api_blueprint.register_blueprint(access_token_blueprint)

# Register accounts apis
account_blueprint = AccountRestApiServer.create()
api_blueprint.register_blueprint(account_blueprint)
app.register_blueprint(api_blueprint)

# Register frontend elements
app.register_blueprint(img_assets_blueprint)
app.register_blueprint(react_blueprint)
