import os
from flask import Flask
from flask_cors import CORS
from bin.blueprints import api_blueprint, img_assets_blueprint, react_blueprint
from modules.config.config_manager import ConfigManager
from modules.account.account_service_manager import AccountServiceManager
from modules.logger.logger_manager import LoggerManager

app = Flask(__name__)
cors = CORS(app)
print('www - attempting to start server...')
print(f'www - node env - {os.environ.get("NODE_ENV")}')
print(f'www - config env - {os.environ.get("NODE_CONFIG_ENV")}')

# Mount deps
ConfigManager.mount_config()
LoggerManager.mount_logger()

# Register accounts apis
account_blueprint = AccountServiceManager.create_rest_api_server()
api_blueprint.register_blueprint(account_blueprint)
app.register_blueprint(api_blueprint)

# Register frontend elements
app.register_blueprint(img_assets_blueprint)
app.register_blueprint(react_blueprint)
