from dataclasses import asdict

from flask import jsonify
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.documentation.documentation_service import DocumentationService


class DocumentationView(MethodView):
    def get(self) -> ResponseReturnValue:
        documentation = DocumentationService.get_documentation()
        documentation_dict = asdict(documentation)
        return jsonify(documentation_dict), 200
