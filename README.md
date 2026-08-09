# Cloud Support and Incident Intelligence Platform

An AWS-hosted cloud support engineering lab demonstrating infrastructure provisioning, Linux administration, application deployment, monitoring, incident troubleshooting, root-cause analysis, and AI-assisted log investigation.

The platform is designed around the responsibilities of a Cloud Support Engineer or Technical Support Engineer supporting a customer-facing SaaS application.

Rather than focusing primarily on application features, the project demonstrates how failures across the application, web server, Linux operating system, networking, permissions, and AWS infrastructure layers can be detected, investigated, resolved, validated, and documented.

---

## Project Overview

The platform runs a Python Flask application on Amazon EC2 behind Gunicorn and an NGINX reverse proxy.

Terraform manages the core AWS infrastructure, IAM access, CloudWatch logging, monitoring, and alerting resources.

AWS Systems Manager Session Manager provides administrative access to the EC2 instance without requiring inbound SSH access.

Amazon CloudWatch collects NGINX access and error logs and monitors EC2 health metrics.

A separate Python-based AI log-intelligence workflow retrieves CloudWatch logs using `boto3` and uses the OpenAI API to assist with:

- Log summarization
- Error-pattern identification
- Root-cause hypotheses
- Severity classification
- Remediation recommendations
- Incident documentation
- Customer-facing incident updates

AI-generated findings are treated as investigation assistance and must be validated against the underlying logs and system evidence.

---

## Project Objectives

This project demonstrates how to:

- Provision AWS infrastructure using Terraform
- Deploy a Python Flask application on Amazon EC2
- Structure a Flask application using an application factory
- Serve Flask through Gunicorn
- Use NGINX as a reverse proxy
- Manage application services using systemd
- Configure HTTPS using Let's Encrypt and Certbot
- Secure administrative EC2 access using AWS Systems Manager
- Attach IAM roles and instance profiles to EC2
- Apply least-privilege CloudWatch log-reading permissions
- Collect NGINX logs in Amazon CloudWatch
- Monitor CPU utilization and EC2 instance health
- Generate CloudWatch alarm actions through Amazon SNS
- Troubleshoot production-style failures using Linux and AWS diagnostics
- Perform structured root-cause analysis
- Document operational incidents
- Use AI to accelerate log investigation while retaining human validation

---

# Architecture

```text
                              Users
                                │
                                ▼
                           DNS / HTTPS
                                │
                                ▼
                      AWS Security Group
                     HTTP 80 / HTTPS 443
                                │
                                ▼
                         NGINX Reverse Proxy
                                │
                                ▼
                              Gunicorn
                       127.0.0.1:5000
                                │
                                ▼
                       Flask Application
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
         Application / Linux             NGINX Access and
              Events                       Error Logs
                                                │
                                                ▼
                                      Amazon CloudWatch Logs
                                                │
                           ┌────────────────────┴─────────────────┐
                           ▼                                      ▼
                  CloudWatch Metrics                      CloudWatch Alarms
                           │                                      │
                           ▼                                      ▼
                    EC2 Monitoring                           SNS Topic

Administrative access:

Engineer
   │
   ▼
AWS Systems Manager
   │
   ▼
Session Manager
   │
   ▼
EC2 Instance

Log analysis:

CloudWatch Logs
      │
      ▼
Python / boto3
      │
      ▼
AI Log Intelligence
      │
      ▼
Incident Analysis / RCA
```

---

# Repository Structure

```text
cloud-support-platform/
├── app/
│   ├── __init__.py                 # Flask application factory
│   ├── app.py                      # WSGI application entry point
│   ├── config.py                   # Environment-driven configuration
│   ├── health.py                   # Application health route
│   └── routes.py                   # General application routes
│
├── terraform/
│   ├── iam.tf                      # IAM role and instance profile
│   ├── main.tf                     # EC2, security group and Elastic IP
│   ├── monitoring.tf               # CloudWatch logs, alarms and SNS
│   ├── outputs.tf                  # Operational Terraform outputs
│   ├── providers.tf
│   ├── terraform.tfvars.example
│   ├── user_data.sh                # EC2 bootstrap configuration
│   ├── variables.tf
│   ├── versions.tf
│   └── README.md
│
├── nginx/                          # NGINX reverse-proxy configuration
├── systemd/                        # Gunicorn systemd service
├── ai-log-intelligence/
│   ├── requirements.txt            # AI/AWS analysis dependencies
│   └── ...                         # CloudWatch/OpenAI analysis workflow
│
├── incident-reports/               # Sanitized incident and RCA reports
├── screenshots/                    # Project validation evidence
├── .gitignore
├── requirements.txt                # Flask/Gunicorn runtime dependencies
└── README.md
```

Local Terraform state, `.tfvars`, virtual environments, logs, private keys, and environment files are excluded from Git.

---

# Implemented Components

## Flask Application Architecture

The Flask application was refactored from a single-file application into a modular package.

```text
app/
├── __init__.py
├── app.py
├── config.py
├── health.py
└── routes.py
```

### Application Factory

`app/__init__.py` contains the Flask application factory:

```python
create_app()
```

The application factory:

1. Creates the Flask application
2. Loads configuration
3. Registers the route blueprints
4. Returns the configured application

This separates application creation from individual routes and makes the code easier to maintain, extend, and test.

---

## Application Configuration

Application configuration is environment-driven where appropriate.

Current configuration includes:

| Variable | Purpose | Default |
|---|---|---|
| `APP_NAME` | Application/service identifier | `flask-support-app` |
| `APP_ENV` | Application environment | `development` |

Example on Linux:

```bash
export APP_NAME="cloud-support-platform"
```

Example using PowerShell:

```powershell
$env:APP_NAME="cloud-support-platform"
```

Environment-specific configuration should not be hardcoded into application source code.

---

## Application Endpoints

The current Flask application exposes three lightweight endpoints.

| Endpoint | Purpose | Expected Result |
|---|---|---|
| `/` | Confirms the web application is responding | HTTP 200 |
| `/health` | Reports application health | HTTP 200 JSON |
| `/skill` | Returns project demonstration metadata | HTTP 200 JSON |

### Health response

```json
{
  "service": "flask-support-app",
  "status": "healthy"
}
```

### Skill response

```json
{
  "service": "flask-support-app",
  "skills": "Technical Support Engineering"
}
```

All three endpoints have been validated locally and through Gunicorn on Amazon Linux.

---

# Local Application Setup

## Create a Virtual Environment

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Runtime Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Validate dependency consistency:

```bash
python -m pip check
```

Expected:

```text
No broken requirements found.
```

---

## Run with the Flask Development Server

From the repository root:

```bash
python -m app.app
```

The application listens locally on:

```text
http://127.0.0.1:5000
```

Validate:

```bash
curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/skill
```

The Flask development server is used only for local validation and is not the production-style WSGI server.

---

# Gunicorn Deployment

Gunicorn is used as the WSGI application server on Linux.

The current WSGI target is:

```text
app.app:app
```

Where:

```text
app.app   → Python module app/app.py
:app      → Flask application object
```

Run Gunicorn from the repository root:

```bash
gunicorn --workers 3 --bind 127.0.0.1:5000 app.app:app
```

Validate the backend:

```bash
curl -i http://127.0.0.1:5000/
curl -i http://127.0.0.1:5000/health
curl -i http://127.0.0.1:5000/skill
```

The refactored application was also validated separately on Amazon Linux using Gunicorn on port `5050`.

All three application endpoints returned:

```text
HTTP/1.1 200 OK
Server: gunicorn
```

This confirmed that the new package structure and WSGI entry point work correctly under Gunicorn rather than only under Flask's development server.

> Gunicorn targets Unix-like operating systems. Local Windows testing uses Flask, while production-style Gunicorn validation is performed on Linux.

---

# systemd Service Management

The application is managed on Amazon Linux using systemd.

The Gunicorn service executes:

```text
app.app:app
```

The relevant service command is:

```ini
ExecStart=/home/ec2-user/flask-support-app/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app.app:app
```

Useful operational commands:

```bash
sudo systemctl status flaskapp
sudo systemctl restart flaskapp
sudo systemctl stop flaskapp
sudo systemctl start flaskapp
```

View application-service logs:

```bash
sudo journalctl -u flaskapp --no-pager -n 100
```

---

# NGINX Reverse Proxy

NGINX is the public-facing web server.

Application traffic follows:

```text
Internet
   ↓
NGINX
   ↓
127.0.0.1:5000
   ↓
Gunicorn
   ↓
Flask
```

The Flask/Gunicorn backend is bound to the loopback interface instead of being directly exposed to the public internet.

NGINX handles public HTTP/HTTPS traffic and forwards application requests to Gunicorn.

---

# Dependency Management

Application runtime dependencies and AI-analysis dependencies are maintained separately.

## Flask Runtime

The root `requirements.txt` contains only direct dependencies required to serve the application:

```text
Flask==3.1.3
gunicorn==23.0.0
```

## AI Log Intelligence

AI-analysis dependencies are stored separately in:

```text
ai-log-intelligence/requirements.txt
```

Current dependencies include:

```text
boto3==1.42.85
openai>=1.66.0
python-dotenv==1.2.2
```

Separating dependency sets keeps the Flask runtime smaller and prevents application servers from installing AWS/AI libraries they do not require.

---

# Infrastructure as Code

Terraform manages the core AWS infrastructure.

Current Terraform resources include:

- Amazon EC2 instance
- EC2 security group
- Elastic IP
- IAM role
- IAM instance profile
- Systems Manager permissions
- CloudWatch Agent permissions
- CloudWatch log-reading permissions
- NGINX CloudWatch Log Groups
- CloudWatch CPU alarm
- CloudWatch EC2 status-check alarm
- Amazon SNS topic
- EC2 user-data bootstrap
- Operational outputs

Terraform configuration is separated into logical files:

```text
terraform/
├── versions.tf
├── providers.tf
├── variables.tf
├── main.tf
├── iam.tf
├── monitoring.tf
├── outputs.tf
└── user_data.sh
```

Detailed infrastructure instructions are available in:

```text
terraform/README.md
```

---

# Secure EC2 Administration

AWS Systems Manager Session Manager is used for administrative access.

The EC2 instance receives an IAM role through an instance profile with:

```text
AmazonSSMManagedInstanceCore
```

The current security group exposes:

```text
TCP 80   HTTP
TCP 443  HTTPS
```

Inbound SSH on TCP port 22 is not required for normal administration.

A Session Manager connection can be started using:

```bash
aws ssm start-session \
  --target <INSTANCE_ID> \
  --region <AWS_REGION>
```

Terraform also provides the Session Manager command as an output.

This approach reduces the need to expose administrative ports publicly and ties access to AWS IAM and Systems Manager.

---

# Terraform Outputs

The current Terraform configuration provides operational outputs including:

- EC2 Instance ID
- Elastic IP
- Public DNS hostname
- Primary application URL
- HTTP application URL
- HTTPS application URL
- `www` HTTPS URL
- Session Manager connection command
- SNS topic ARN

Example:

```bash
terraform output
```

Sensitive credentials and private keys are not exposed through Terraform outputs.

---

# DNS and HTTPS

The application is accessed through a custom domain over HTTPS.

The current Terraform configuration accepts the domain name as an input and generates application URLs from it.

DNS management itself remains external to the current Terraform configuration.

HTTPS is provided using:

- NGINX
- Let's Encrypt
- Certbot

The application supports HTTP-to-HTTPS redirection.

Useful validation commands include:

```bash
curl -I http://<domain>
curl -I https://<domain>
```

and:

```bash
nslookup <domain>
```

or:

```bash
dig <domain>
```

---

# Monitoring and Alerting

Amazon CloudWatch provides infrastructure and web-server visibility.

## CloudWatch Log Groups

Terraform manages:

```text
/ec2/flask-nginx/access
/ec2/flask-nginx/error
```

The log groups currently use a 14-day retention period.

The CloudWatch Agent running on EC2 sends NGINX logs into these log groups.

---

## CloudWatch Agent

The EC2 bootstrap process installs and configures the Amazon CloudWatch Agent.

The agent currently collects:

- NGINX access logs
- NGINX error logs

The EC2 IAM role receives:

```text
CloudWatchAgentServerPolicy
```

to allow the CloudWatch Agent to publish operational data.

---

## CPU Alarm

Terraform manages an EC2 CPU utilization alarm.

Current threshold:

```text
CPUUtilization >= 80%
```

for two consecutive five-minute evaluation periods.

---

## EC2 Status-Check Alarm

Terraform also monitors:

```text
StatusCheckFailed
```

This can identify instance-level or underlying AWS host health problems.

---

## Amazon SNS

CloudWatch alarm actions are connected to a dedicated Amazon SNS topic.

The SNS topic ARN is exposed as a Terraform output.

Subscriber delivery, such as email notification, can be configured separately.

---

# AI-Assisted Log Intelligence

The project includes a Python workflow that retrieves CloudWatch logs using `boto3` and analyzes operational events using the OpenAI API.

The EC2 IAM role includes scoped permissions that allow the analyzer to read the project's NGINX CloudWatch log groups.

## Current Capabilities

The workflow can assist with:

- Total request analysis
- Successful versus failed request counts
- HTTP status-code breakdown
- Peak traffic identification
- Error-pattern detection
- Anomaly identification
- Root-cause hypotheses
- Severity classification
- Recommended remediation
- Suggested AWS/Linux diagnostic commands
- Structured incident reports
- Customer-facing incident updates

AI output is not treated as authoritative.

Findings must be validated against:

- CloudWatch logs
- NGINX logs
- Linux service state
- Network tests
- Application behavior
- Infrastructure configuration

---

# Production-Style Incidents Investigated

The `incident-reports/` directory contains sanitized reports documenting controlled troubleshooting exercises performed in the lab.

These are lab simulations and do not claim that real customer production systems were affected.

---

## SSH / Private-IP Connectivity Failure

**Symptom:** SSH connection timed out.

**Root cause:** A private EC2 IP address was used from outside the VPC.

**Investigation included:**

- ICMP/network testing
- Public versus private IP validation
- AWS networking analysis

**Resolution:** Used the correct reachable endpoint and validated network access.

---

## Linux Permission Failure

**Symptom:** Administrative service-management commands returned access-denied errors.

**Root cause:** Commands requiring elevated permissions were executed without `sudo`.

**Resolution:** Used appropriate privilege escalation and systemd commands.

---

## Flask / Gunicorn Backend Outage

**Symptom:** Application became unavailable behind NGINX.

**Root cause:** The Gunicorn/Flask backend service was stopped.

**Evidence included:**

- systemd status
- process inspection
- NGINX logs
- direct backend testing

**Resolution:** Restored the backend service and validated application availability.

---

## HTTP 502 Bad Gateway

**Symptom:**

```text
HTTP 502 Bad Gateway
```

**Root cause:** NGINX was running but could not connect to the Gunicorn backend.

NGINX reported upstream connection failures to:

```text
127.0.0.1:5000
```

**Resolution:**

- Confirmed NGINX was healthy
- Verified the backend service state
- Reviewed NGINX error logs
- Restored Gunicorn
- Confirmed HTTP 200 recovery

---

## NGINX Connection Refusal

**Symptom:** HTTP requests returned connection-refused errors.

**Root cause:** NGINX was stopped and nothing was listening on the public web port.

**Resolution:**

- Inspected NGINX service state
- Verified listening ports
- Restarted NGINX
- Confirmed HTTP recovery

---

## NGINX Restart Timeout

**Symptom:** NGINX did not stop cleanly during a restart.

**Investigation included:**

- `systemctl status`
- `journalctl`
- process inspection
- systemd timeout behavior

The service eventually required forced process termination before being restarted successfully.

---

## CloudWatch IAM Permission Failure

**Symptom:** The log-analysis workflow could not retrieve CloudWatch logs.

**Root cause:** Required IAM permissions were missing.

**Resolution:** Added scoped CloudWatch Logs permissions and validated access.

---

## DNS / HTTPS Migration Validation

A replacement EC2 deployment required validation across:

- Elastic IP
- DNS
- NGINX
- HTTPS
- application availability

The exercise demonstrated how infrastructure replacement can affect multiple layers even when the application itself is healthy.

---

# Application Startup Troubleshooting

When the Flask/Gunicorn application does not start, the following workflow can be used.

## Verify Python Imports

```bash
python -c "from app.app import app; print(app)"
```

---

## Verify Registered Routes

```bash
python -c "from app import create_app; app=create_app(); print(app.url_map)"
```

Expected application routes currently include:

```text
/
/health
/skill
```

---

## Verify Python Dependencies

```bash
python -m pip check
```

Expected:

```text
No broken requirements found.
```

---

## Test Gunicorn Directly

```bash
gunicorn --workers 3 --bind 127.0.0.1:5000 app.app:app
```

---

## Check systemd

```bash
sudo systemctl status flaskapp
```

View recent logs:

```bash
sudo journalctl -u flaskapp --no-pager -n 100
```

---

## Check the Backend Port

```bash
ss -lntp | grep 5000
```

---

## Test Gunicorn Without NGINX

```bash
curl -i http://127.0.0.1:5000/health
```

If this succeeds but the public application fails, the investigation can move toward:

- NGINX configuration
- TLS
- DNS
- security groups
- public networking

If the backend test fails, the investigation remains focused on:

- Gunicorn
- Flask
- Python dependencies
- systemd
- application configuration

---

# Troubleshooting Methodology

The general incident-investigation process moves through each technical layer:

```text
1. Confirm the reported symptom
2. Reproduce the failure
3. Validate DNS resolution
4. Test network reachability
5. Review AWS security controls
6. Validate listening ports
7. Check NGINX service health
8. Check Gunicorn / Flask health
9. Test the backend directly
10. Inspect systemd and journal logs
11. Inspect NGINX access and error logs
12. Review CloudWatch logs and alarms
13. Isolate the failure domain
14. Apply remediation
15. Validate service recovery
16. Document root cause
17. Record preventative actions
18. Prepare a customer-facing update
```

This layered approach helps determine whether a failure originates from:

```text
Customer / DNS
      ↓
Network
      ↓
AWS infrastructure
      ↓
NGINX
      ↓
Gunicorn
      ↓
Flask
      ↓
Application configuration
```

---

# Security Practices

The repository is designed to remain safe for public GitHub use.

The `.gitignore` excludes:

```text
.env
.env.*
*.pem
*.key
.terraform/
*.tfstate
*.tfstate.*
*.tfvars
*.tfplan
.venv/
venv/
__pycache__/
*.pyc
```

Public-safe example files such as:

```text
terraform.tfvars.example
```

remain tracked.

Before committing infrastructure changes, tracked files can be checked with:

```powershell
git ls-files |
    Select-String -Pattern '(\.env$|\.pem$|\.key$|\.tfstate|\.tfvars$)'
```

A clean result returns no sensitive tracked files.

---

# Technology Stack

## Cloud and Infrastructure

- AWS EC2
- AWS IAM
- AWS Systems Manager
- AWS Security Groups
- Elastic IP
- Amazon CloudWatch
- Amazon SNS
- Terraform

## Application

- Python
- Flask
- Gunicorn

## Web and Networking

- NGINX
- DNS
- TCP/IP
- HTTP/HTTPS
- SSL/TLS
- Let's Encrypt
- Certbot

## Linux Operations

- Amazon Linux
- systemd
- `systemctl`
- `journalctl`
- `curl`
- `ss`
- `ps`
- `tail`
- `grep`

## Automation and AI

- Python
- Bash
- `boto3`
- OpenAI API
- OpenAI Python SDK

---

# Skills Demonstrated

- AWS infrastructure provisioning
- Infrastructure as code
- Terraform
- Linux administration
- Systems Manager Session Manager
- IAM roles and instance profiles
- Production-style application deployment
- Flask application architecture
- Gunicorn WSGI deployment
- NGINX reverse-proxy troubleshooting
- systemd service management
- DNS and HTTPS troubleshooting
- CloudWatch logging
- Cloud monitoring and alerting
- IAM permission investigation
- Log analysis
- Incident triage
- Root-cause analysis
- Service recovery
- Customer-impact assessment
- Technical documentation
- Customer-facing incident communication
- AI-assisted operational analysis

---

# Current Limitations

This project currently uses a single EC2 instance and is intentionally designed as a support-engineering lab rather than a highly available production architecture.

It does not yet provide:

- Application Load Balancer
- Auto Scaling
- Multi-AZ application deployment
- Automated failover
- Docker-based application deployment
- Container orchestration
- PostgreSQL application persistence
- Complete automated test coverage
- Fully automated CI/CD
- Zero-downtime deployment
- Distributed tracing

These limitations are documented intentionally so future architecture is not represented as currently implemented functionality.

---

# Development Roadmap

## Application Health and Support APIs

Planned improvements include:

- `/healthz`
- `/readyz`
- `/api/v1/status`
- Real dependency readiness checks

---

## Application Packaging

- Production Dockerfile
- Non-root container execution
- Docker health checks
- Docker Compose
- Flask/Gunicorn container
- NGINX container
- PostgreSQL container

---

## Developer Support Scenarios

- REST API event endpoints
- API-key authentication
- Webhook receiver
- HMAC signature validation
- PostgreSQL event persistence
- Postman collection
- Controlled HTTP failure simulations

---

## Testing and Security

- Pytest test coverage
- Ruff linting
- Bandit security scanning
- `pip-audit`
- Dependency vulnerability review

---

## CI/CD

- GitHub Actions
- Automated Pytest execution
- Ruff validation
- Bandit scanning
- `pip-audit`
- Docker build validation
- Terraform formatting and validation

---

## Observability

- Structured JSON application logging
- Request correlation IDs
- Request latency metrics
- HTTP 4xx/5xx metrics
- Webhook metrics
- Readiness metrics
- CloudWatch operational dashboard
- Additional service-level alarms

---

## Future Architecture Exploration

Potential future architecture improvements include:

- Application Load Balancer
- Auto Scaling Group
- ECS
- Kubernetes
- Multi-AZ architecture
- Managed database services

These are roadmap items and are not represented as currently implemented functionality.

---

# Why This Project Matters

Technical Support Engineers and Cloud Support Engineers frequently investigate failures that cross multiple technical layers.

A customer may report only:

```text
"The application isn't working."
```

The underlying problem could exist in:

- DNS
- TLS
- Networking
- AWS security controls
- Linux
- NGINX
- Gunicorn
- Flask
- IAM
- Monitoring configuration
- Application configuration

This project demonstrates an end-to-end support workflow:

```text
Customer symptom
      ↓
Request reproduction
      ↓
DNS / network validation
      ↓
AWS infrastructure validation
      ↓
Linux service validation
      ↓
NGINX / Gunicorn / Flask isolation
      ↓
Log and metric analysis
      ↓
Root-cause identification
      ↓
Service recovery
      ↓
Validation
      ↓
Corrective action
      ↓
Incident documentation
      ↓
Customer communication
```

The goal is not simply to deploy a Flask application.

The goal is to demonstrate the ability to **operate, troubleshoot, secure, monitor, and support a customer-facing cloud service**.

---

# Author

**Edikan Ekong**

AWS Certified Cloud Practitioner

Technical Support Engineer | Cloud Support Engineer | Platform Support Engineer