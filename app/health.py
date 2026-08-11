import time
from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify


health_bp = Blueprint("health", __name__)


def _utc_timestamp():
    """Return the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _uptime_seconds():
    """Return application uptime in seconds."""
    start_time = current_app.config["START_TIME_MONOTONIC"]

    return round(time.monotonic() - start_time, 3)


def _dependency_status():
    """
    Check dependencies required for the Flask application to serve requests.

    Configuration is currently the only required application dependency.
    Database and external service checks are placeholders until those
    dependencies are actually implemented.
    """

    required_config = [
        "APP_NAME",
        "APP_ENV",
        "APP_VERSION",
    ]

    missing_config = [
        key
        for key in required_config
        if not str(current_app.config.get(key, "")).strip()
    ]

    configuration = {
        "required": True,
        "status": "healthy" if not missing_config else "unhealthy",
    }

    if missing_config:
        configuration["missing"] = missing_config

    return {
        "configuration": configuration,
        "database": {
            "required": False,
            "status": "not_configured",
        },
        "external_services": {
            "required": False,
            "status": "not_configured",
        },
    }


def _is_ready(dependencies):
    """Return True when every required dependency is healthy."""
    return all(
        dependency["status"] == "healthy"
        for dependency in dependencies.values()
        if dependency.get("required")
    )


@health_bp.route("/health")
def health():
    """Legacy health endpoint retained for compatibility."""
    return jsonify(
        {
            "service": current_app.config["APP_NAME"],
            "status": "healthy",
        }
    ), 200


@health_bp.route("/healthz")
def healthz():
    """Basic application health/liveness endpoint."""
    return jsonify(
        {
            "application": current_app.config["APP_NAME"],
            "status": "healthy",
            "timestamp": _utc_timestamp(),
        }
    ), 200


@health_bp.route("/readyz")
def readyz():
    """Readiness endpoint that validates required dependencies."""
    dependencies = _dependency_status()
    ready = _is_ready(dependencies)

    response = {
        "application": current_app.config["APP_NAME"],
        "status": "ready" if ready else "not_ready",
        "dependencies": dependencies,
        "timestamp": _utc_timestamp(),
    }

    return jsonify(response), 200 if ready else 503


@health_bp.route("/api/v1/status")
def application_status():
    """Return detailed operational status information."""
    dependencies = _dependency_status()
    ready = _is_ready(dependencies)

    response = {
        "application": current_app.config["APP_NAME"],
        "version": current_app.config["APP_VERSION"],
        "status": "healthy" if ready else "degraded",
        "uptime_seconds": _uptime_seconds(),
        "environment": current_app.config["APP_ENV"],
        "dependencies": dependencies,
        "timestamp": _utc_timestamp(),
    }

    return jsonify(response), 200 if ready else 503