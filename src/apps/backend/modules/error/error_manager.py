from flask import Flask, Response, jsonify

from modules.error.custom_errors import AppError, MissingKeyError, ValueTypeMismatchError


class ErrorManager:
    @staticmethod
    def mount_error_handler(app: Flask) -> None:
        app.register_error_handler(AppError, ErrorManager._application_error)
        app.register_error_handler(Exception, ErrorManager._unhandled_exception_handler)
        app.register_error_handler(MissingKeyError, ErrorManager._missing_key_error)
        app.register_error_handler(ValueTypeMismatchError, ErrorManager._type_mismatch_error)

    @staticmethod
    def _unhandled_exception_handler(error: Exception) -> Response:
        return jsonify({"message": str(error), "code": 500})

    @staticmethod
    def _type_mismatch_error(error: ValueTypeMismatchError) -> Response:
        return jsonify({"message": str(error), "code": error.code})

    @staticmethod
    def _missing_key_error(error: MissingKeyError) -> Response:
        return jsonify({"message": str(error), "code": error.code})

    @staticmethod
    def _application_error(error: AppError) -> Response:
        return jsonify({"message": error.message, "code": error.code})
