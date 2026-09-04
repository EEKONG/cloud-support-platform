import os
import re
from collections import Counter
from datetime import datetime, timedelta, timezone

import boto3
from flask import Blueprint, jsonify, request


logs_bp = Blueprint("logs", __name__)

AWS_REGION = os.getenv("AWS_REGION", "ca-central-1")
LOG_API_KEY = os.getenv("LOG_API_KEY")

ACCESS_LOG_GROUP = "/ec2/flask-nginx/access"
ERROR_LOG_GROUP = "/ec2/flask-nginx/error"

STATUS_CODE_PATTERN = re.compile(r'" (\d{3}) ')


def _authorized():
    supplied_key = request.headers.get("X-API-Key")
    return LOG_API_KEY and supplied_key == LOG_API_KEY


def _get_cloudwatch_events(log_group_name, minutes=60):
    logs_client = boto3.client("logs", region_name=AWS_REGION)

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)

    response = logs_client.filter_log_events(
        logGroupName=log_group_name,
        startTime=int(start_time.timestamp() * 1000),
        endTime=int(end_time.timestamp() * 1000),
        limit=500,
    )

    return response.get("events", [])


def _format_event(event):
    timestamp_ms = event.get("timestamp")

    timestamp = None

    if timestamp_ms:
        timestamp = datetime.fromtimestamp(
            timestamp_ms / 1000,
            timezone.utc,
        ).isoformat().replace("+00:00", "Z")

    return {
        "timestamp": timestamp,
        "message": event.get("message", "").strip(),
    }


def _calculate_access_metrics(events):
    status_counts = Counter()

    for event in events:
        message = event.get("message", "")

        match = STATUS_CODE_PATTERN.search(message)

        if match:
            status_counts[match.group(1)] += 1

    successful_requests = sum(
        count
        for code, count in status_counts.items()
        if code.startswith("2") or code.startswith("3")
    )

    client_errors = sum(
        count
        for code, count in status_counts.items()
        if code.startswith("4")
    )

    server_errors = sum(
        count
        for code, count in status_counts.items()
        if code.startswith("5")
    )

    return {
        "total_requests": sum(status_counts.values()),
        "successful_requests": successful_requests,
        "client_errors": client_errors,
        "server_errors": server_errors,
        "status_counts": dict(sorted(status_counts.items())),
    }


def _calculate_upstream_errors(events):
    upstream_errors = Counter()

    for event in events:
        message = event.get("message", "").lower()

        if (
            "connection refused" in message
            and "upstream" in message
        ):
            upstream_errors["connection_refused"] += 1

        if "upstream timed out" in message:
            upstream_errors["upstream_timeout"] += 1

        if "no live upstreams" in message:
            upstream_errors["no_live_upstreams"] += 1

        if "upstream prematurely closed connection" in message:
            upstream_errors["premature_connection_close"] += 1

    return {
        "total_upstream_errors": sum(upstream_errors.values()),
        "error_types": dict(upstream_errors),
    }


@logs_bp.route("/api/v1/logs/recent")
def recent_logs():

    if not _authorized():
        return jsonify({"error": "unauthorized"}), 401

    try:
        window_minutes = 60

        access_events = _get_cloudwatch_events(
            ACCESS_LOG_GROUP,
            minutes=window_minutes,
        )

        error_events = _get_cloudwatch_events(
            ERROR_LOG_GROUP,
            minutes=window_minutes,
        )

        access_metrics = _calculate_access_metrics(access_events)
        upstream_metrics = _calculate_upstream_errors(error_events)

        recent_access_logs = [
            _format_event(event)
            for event in access_events[-50:]
        ]

        recent_error_logs = [
            _format_event(event)
            for event in error_events[-50:]
        ]

        return jsonify(
            {
                "status": "success",
                "window_minutes": window_minutes,
                "metrics": {
                    **access_metrics,
                    "upstream_errors": upstream_metrics,
                },
                "access_logs": {
                    "log_group": ACCESS_LOG_GROUP,
                    "recent": recent_access_logs,
                },
                "error_logs": {
                    "log_group": ERROR_LOG_GROUP,
                    "recent": recent_error_logs,
                },
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat().replace("+00:00", "Z"),
            }
        ), 200

    except Exception as exc:
        return jsonify(
            {
                "status": "error",
                "message": str(exc),
            }
        ), 500