import time

from flask import Flask

from .config import Config
from .health import health_bp
from .routes import main_bp
from .logs import logs_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Monotonic time is used for measuring application uptime.
    app.config["START_TIME_MONOTONIC"] = time.monotonic()

    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(logs_bp)

    return app