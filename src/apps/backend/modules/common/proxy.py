from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from modules.config.config_service import ConfigService

class Proxy:
    @staticmethod
    def apply_proxy_if_enabled(app: Flask) -> Flask:
        """
        Enables ProxyFix middleware on the provided Flask app.

        Args:
            app (Flask): The Flask app instance to which the middleware will be applied.
        Returns:
            Flask: The Flask app instance with ProxyFix applied, if enabled by configuration.
        """
        if ConfigService.has_key("USE_PROXY") and ConfigService.get_bool("USE_PROXY"):
            app.wsgi_app = ProxyFix(app.wsgi_app) # type: ignore
        return app
