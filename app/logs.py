import os
from collections import Counter
from datetime import datetime, timedelta, timezone

import boto3
from flask import Blueprint, jsonify, request


logs_bp = Blueprint("logs", __name__)

AWS_REGION = os.getenv("AWS_REGION", "ca-central-1")
LOG_API_KEY = os.getenv("LOG_API_KEY")

LOG_GROUPS = [
    "/ec2/flask-nginx/access",
    "/ec2/flask-nginx/error",
]


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


def _calculate_metrics(events):
    status_counts = Counter()
    raw_logs = []

    for event in events:
        message = event.get("message", "").strip()

        if message:
            raw_logs.append(message)

        for part in message.split():
            if part.isdigit() and len(part) == 3:
                status_counts[part] += 1
                break

    total_requests = sum(status_counts.values())

    successful_requests = sum(
        count
        for code, count in status_counts.items()
        if code.startswith("2") or code.startswith("3")
    )

    failed_requests = sum(
        count
        for code, count in status_counts.items()
        if code.startswith("4") or code.startswith("5")
    )

    return {
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "status_counts": dict(status_counts),
        "recent_log_lines": raw_logs[-100:],
    }


@logs_bp.route("/api/v1/logs/recent")
def recent_logs():

    if not _authorized():
        return jsonify({"error": "unauthorized"}), 401

    try:
        all_events = []

        for log_group in LOG_GROUPS:
            events = _get_cloudwatch_events(
                log_group,
                minutes=60,
            )
            all_events.extend(events)

        metrics = _calculate_metrics(all_events)

        return jsonify(
            {
                "status": "success",
                "window_minutes": 60,
                "log_groups": LOG_GROUPS,
                "metrics": metrics,
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