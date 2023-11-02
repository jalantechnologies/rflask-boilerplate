from flask import Flask
from flask_cors import CORS
from bin.blueprints import api_blueprint, img_assets_blueprint, react_blueprint

from modules.account.account_service_manager import AccountServiceManager

app = Flask(__name__)
cors = CORS(app)


# Register experience apps
app.register_blueprint(img_assets_blueprint)
app.register_blueprint(react_blueprint)

# Register account apps
account_blueprint = AccountServiceManager.create_rest_api_server()
api_blueprint.register_blueprint(account_blueprint)

app.register_blueprint(api_blueprint)
