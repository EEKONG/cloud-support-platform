# AI Log Intelligence

## Overview

This module analyzes AWS CloudWatch Logs from an EC2-hosted NGINX and Flask application using Python, boto3, and the OpenAI API.

It retrieves recent CloudWatch log events, calculates request metrics, and generates an AI-powered support incident report.

## Features

- Pulls NGINX access and error logs from CloudWatch
- Counts successful and failed requests
- Breaks down HTTP status codes
- Identifies peak traffic windows
- Summarizes connection activity
- Detects errors and suspicious traffic
- Generates root cause analysis
- Recommends AWS/Linux troubleshooting commands
- Produces customer-facing updates

## Architecture

```text
CloudWatch Logs
      │
      ▼
Python boto3 Collector
      │
      ▼
Metrics Parser
      │
      ▼
OpenAI API
      │
      ▼
AI Incident Report