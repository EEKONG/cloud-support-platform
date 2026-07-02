# AWS EC2 + NGINX + Flask Production Deployment with AI Log Intelligence

## Project Overview

This project demonstrates the deployment, monitoring, and operational support of a production-style Flask application hosted on AWS EC2 using NGINX as a reverse proxy, Gunicorn as the application server, Let's Encrypt SSL certificates, Amazon CloudWatch monitoring, and OpenAI-powered AI Log Intelligence.

The project showcases end-to-end cloud infrastructure deployment, production support, observability, incident analysis, and AI-assisted troubleshooting commonly performed by Cloud Support Engineers, Technical Support Engineers, and Site Reliability Engineers (SREs).

---

# Architecture

```text
                        Internet
                            │
                            ▼
                  AWS Security Group
                  (Ports 80 / 443)
                            │
                            ▼
                   NGINX Reverse Proxy
                            │
                            ▼
                        Gunicorn
                   (127.0.0.1:5000)
                            │
                            ▼
                    Flask Application
                            │
                            ▼
                  Amazon CloudWatch Logs
                            │
                            ▼
                  Python + boto3 Collector
                            │
                            ▼
                 OpenAI Log Intelligence
                            │
                            ▼
         AI Incident Report & Root Cause Analysis
```

---

# Technologies Used

## Cloud

- AWS EC2
- Amazon CloudWatch
- IAM
- CloudWatch Logs

## AI

- OpenAI API
- OpenAI Python SDK

## Web & Application

- Python
- Flask
- Gunicorn
- NGINX

## Linux & Operations

- Amazon Linux
- systemd
- SSH
- journalctl
- curl
- boto3

## Security

- Let's Encrypt
- Certbot
- HTTPS / TLS

---

# Features

## Infrastructure

- Flask application deployment
- Gunicorn application server
- NGINX reverse proxy
- HTTPS using Let's Encrypt
- Automatic HTTP → HTTPS redirection
- systemd service management

## Monitoring

- CloudWatch metrics
- CloudWatch alarms
- CloudWatch log aggregation
- Health monitoring

## AI Log Intelligence

- Retrieve NGINX logs from CloudWatch
- AI-powered connection summaries
- Incident detection
- Error analysis
- Root cause analysis
- Severity classification
- Recommended remediation
- Suggested AWS/Linux diagnostic commands
- Customer-facing incident updates

---

# Application Endpoints

| Endpoint | Description |
|----------|-------------|
| / | Landing Page |
| /health | Health Check |
| /skill | Sample API Endpoint |

---

# Deployment Process

## 1. Launch EC2

- Amazon Linux EC2
- Configure Security Groups
    - SSH (22)
    - HTTP (80)
    - HTTPS (443)

## 2. Install Dependencies

```bash
sudo dnf update -y
sudo dnf install nginx python3 python3-pip git -y
```

## 3. Configure Python

```bash
python3 -m venv venv
source venv/bin/activate

pip install flask
pip install gunicorn
pip install boto3
pip install openai
pip install python-dotenv
```

## 4. Deploy Flask

```bash
gunicorn --workers 3 --bind 127.0.0.1:5000 app:app
```

## 5. Configure NGINX

- Reverse Proxy
- SSL Termination
- HTTP → HTTPS Redirect
- Proxy to Gunicorn

## 6. Configure systemd

```bash
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
```

## 7. Configure HTTPS

```bash
sudo certbot --nginx
```

Validate:

```bash
sudo certbot renew --dry-run
```

---

# CloudWatch Monitoring

## Metrics

- CPU
- Memory
- Disk

## Alarms

- High CPU
- High Memory
- High Disk

## Log Groups

- /ec2/flask-nginx/access
- /ec2/flask-nginx/error

---

# AI Log Intelligence

The project includes an AI-powered log analysis module that retrieves CloudWatch logs using boto3 and analyzes them using the OpenAI API.

### Example Output

The AI generates:

- Executive Summary
- Connection Activity
- Errors & Anomalies
- Root Cause Analysis
- Severity Assessment
- Recommended Actions
- AWS/Linux Diagnostic Commands
- Customer Status Update

---

# Troubleshooting Scenarios

## 502 Bad Gateway

Resolved by:

- Verifying Gunicorn
- Reviewing NGINX configuration
- Inspecting CloudWatch logs

---

## SSL Validation

Resolved by:

- Validating DNS
- Configuring Certbot
- Testing certificate renewal

---

## AI Log Analysis

Example workflow:

```text
CloudWatch Logs
      │
      ▼
Python Collector
      │
      ▼
OpenAI Analysis
      │
      ▼
Incident Report
```

---

# Security

- Gunicorn bound to localhost
- HTTPS enforced
- CloudWatch IAM permissions
- Security Groups
- Environment variables
- API keys excluded from Git
- SSL auto-renewal

---

# Skills Demonstrated

- AWS EC2
- CloudWatch
- CloudWatch Logs
- IAM
- Python
- Flask
- Gunicorn
- NGINX
- Linux Administration
- HTTPS / TLS
- OpenAI API
- AI Log Intelligence
- boto3
- Incident Response
- Root Cause Analysis
- Production Support
- Observability

---

# Future Enhancements

- Terraform
- GitHub Actions CI/CD
- Docker
- Kubernetes
- Route 53
- AWS Systems Manager
- CloudWatch Dashboards
- Slack / Microsoft Teams Incident Notifications
- AI Security Analysis
- AI Performance Analysis
- AI Anomaly Detection

---

# Author

**Edikan Ekong**

AWS Certified Cloud Practitioner

Cloud Support Engineering | Platform Support | AI-Powered Operations | Technical Support Engineering