import os
from collections import Counter
from datetime import datetime, timedelta, timezone

import boto3
from dotenv import load_dotenv
from openai import OpenAI

from prompts import CLOUDWATCH_LOG_ANALYSIS_PROMPT


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ca-central-1")

LOG_GROUPS = [
    "/ec2/flask-nginx/access",
    "/ec2/flask-nginx/error"
]

client = OpenAI(api_key=OPENAI_API_KEY)
logs_client = boto3.client("logs", region_name=AWS_REGION)


def get_cloudwatch_events(log_group_name, minutes=60):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)

    response = logs_client.filter_log_events(
        logGroupName=log_group_name,
        startTime=int(start_time.timestamp() * 1000),
        endTime=int(end_time.timestamp() * 1000),
        limit=500
    )

    return response.get("events", [])


def calculate_metrics(events):
    status_counts = Counter()
    minute_counts = Counter()
    raw_log_lines = []

    for event in events:
        message = event.get("message", "")
        timestamp = event.get("timestamp")

        raw_log_lines.append(message)

        if timestamp:
            minute = datetime.fromtimestamp(
                timestamp / 1000,
                timezone.utc
            ).strftime("%H:%M UTC")
            minute_counts[minute] += 1

        for part in message.split():
            if part.isdigit() and len(part) == 3:
                status_counts[part] += 1
                break

    total_requests = sum(status_counts.values())

    successful_requests = sum(
        count for code, count in status_counts.items()
        if code.startswith("2") or code.startswith("3")
    )

    failed_requests = sum(
        count for code, count in status_counts.items()
        if code.startswith("4") or code.startswith("5")
    )

    if minute_counts:
        peak_time, peak_count = minute_counts.most_common(1)[0]
    else:
        peak_time, peak_count = "N/A", 0

    return {
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "status_counts": dict(status_counts),
        "peak_time": peak_time,
        "peak_count": peak_count,
        "raw_log_lines": raw_log_lines
    }


def build_prompt(metrics):
    status_breakdown = "\n".join(
        f"- {code}: {count}"
        for code, count in sorted(metrics["status_counts"].items())
    )

    if not status_breakdown:
        status_breakdown = "- No HTTP status codes detected"

    raw_logs = "\n".join(metrics["raw_log_lines"][-200:])

    return CLOUDWATCH_LOG_ANALYSIS_PROMPT.format(
        total_requests=metrics["total_requests"],
        successful_requests=metrics["successful_requests"],
        failed_requests=metrics["failed_requests"],
        peak_time=metrics["peak_time"],
        peak_count=metrics["peak_count"],
        status_breakdown=status_breakdown,
        raw_logs=raw_logs
    )


def main():
    all_events = []

    for group in LOG_GROUPS:
        events = get_cloudwatch_events(group, minutes=60)
        all_events.extend(events)

    metrics = calculate_metrics(all_events)
    prompt = build_prompt(metrics)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    print(response.output_text)


if __name__ == "__main__":
    main()