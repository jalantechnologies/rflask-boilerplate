from flask import Blueprint, Flask

app = Flask(__name__)
blueprint = Blueprint("blueprint", __name__, url_prefix="")
blueprint.add_url_rule("/", "", view_func=lambda: "<h3> Start your development... </h3>")

app.register_blueprint(blueprint)
