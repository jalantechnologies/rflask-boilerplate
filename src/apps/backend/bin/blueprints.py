import os
import json
from werkzeug.wrappers import Response

from typing import Union
from flask import Blueprint, send_from_directory

# Serve react
react_public_dir_path: str = "../../../dist/public/"
react_public_dir: str = os.path.join(os.getcwd(), react_public_dir_path)
react_blueprint = Blueprint('react', __name__, static_folder=react_public_dir, url_prefix="/")


@react_blueprint.route('/', defaults={'path': ''})
@react_blueprint.route('/<path:path>')
def serve_react_home(path: Union[os.PathLike, str]) -> Response:
  assert react_blueprint.static_folder, "Unable to resolve react root path"
  return send_from_directory(react_blueprint.static_folder, 'index.html')


@react_blueprint.route('/index.bundle.js')
def serve_js_bundle() -> Response:
  assert react_blueprint.static_folder, "Unable to resolve react root path"
  return send_from_directory(react_blueprint.static_folder, 'index.bundle.js')


# Server react static images
react_img_assets_path: str = '../../../dist/assets/img'
react_img_assets_dir: str = os.path.join(os.getcwd(), '../../../dist/assets/img')
img_assets_blueprint = Blueprint("image_assets", __name__, static_folder=react_img_assets_dir, url_prefix="/assets")


@img_assets_blueprint.route('/assets/img/<path:filename>')
def serve_static_images(filename: Union[os.PathLike, str]) -> Response:
  assert img_assets_blueprint.static_folder, "Unable to resolve react root path"
  return send_from_directory(img_assets_blueprint.static_folder, filename)


# Serve Api home page
api_blueprint = Blueprint("api", __name__, url_prefix="/api")


@api_blueprint.route("/")
def serve_api_home() -> Response:
  message = {
    "msg": "Start your development..."
  }
  return Response(json.dumps(message), status=200)
