# app/__init__.py
from flask import Flask
from config import DevelopmentConfig
from .data_loader import load_data
import plotly.io as pio

pio.templates.default = "plotly_white"

# Load data once on application startup
DATA = load_data()

def create_app(config_class=DevelopmentConfig):
    """Creates and configures an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        # Import and register routes
        from . import routes
        app.register_blueprint(routes.main_bp)

    return app

