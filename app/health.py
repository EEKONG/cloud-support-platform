from flask import Blueprint, current_app

health_bp = Blueprint("health", __name__)


@health_bp.route("/health")
def health():
    return {
        "status": "healthy",
        "service": current_app.config["APP_NAME"],
    }, 200