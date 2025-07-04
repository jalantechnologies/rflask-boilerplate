from src.apps.backend.scripts.application.setup_app import setup

def pytest_configure(config):
    setup() 