# Incident Reports

Production-style incident documentation from the **Cloud Support and Incident Intelligence Platform**, an AWS support-engineering lab built with EC2, Amazon Linux, NGINX, Gunicorn, Flask, systemd, CloudWatch, Terraform, DNS, TLS, Python, and AI-assisted log analysis.

> **Disclosure:** These reports describe controlled lab simulations and troubleshooting exercises. They do not claim that real customers or production systems were affected.

## What This Folder Demonstrates

Each report follows an operational support workflow:

```text
Symptom
  → impact assessment
  → reproduction
  → evidence collection
  → failure-domain isolation
  → root-cause analysis
  → recovery
  → validation
  → prevention
  → communication
```

The reports intentionally include commands, sanitized outputs, rejected hypotheses, recovery checks, and follow-up actions. The goal is to show how a Technical Support Engineer or Cloud Support Engineer investigates an issue—not merely state the final fix.

## Incident Index

| ID | Scenario | Layer | Symptom | Confirmed cause |
|---|---|---|---|---|
| [INC-001](INC-001-ssh-private-ip-timeout.md) | SSH timeout using a private EC2 address | Networking/access | SSH timed out | A private VPC address was used from outside the VPC |
| [INC-002](INC-002-nginx-permission-and-service-validation.md) | NGINX command denied | Linux/permissions | `systemctl` returned `Access denied` | Administrative commands were run without `sudo` |
| [INC-003](INC-003-flask-gunicorn-backend-outage-502.md) | Flask/Gunicorn backend outage | Application/proxy | NGINX returned HTTP 502 | Gunicorn was stopped and port 5000 had no listener |
| [INC-004](INC-004-nginx-down-connection-refused.md) | NGINX service outage | Web server | Port 80 returned connection refused | NGINX was stopped |
| [INC-005](INC-005-nginx-restart-timeout.md) | NGINX restart timeout | Service management | systemd forced process termination | NGINX did not exit within the stop timeout |
| [INC-006](INC-006-cloudwatch-iam-and-ai-log-analysis.md) | Log-analysis access failure | IAM/observability | CloudWatch access denied; API key missing | Required IAM action and runtime variable were absent |
| [INC-007](INC-007-dns-https-and-ec2-migration-validation.md) | Domain timeout after EC2 migration | DNS/network/TLS | Domain was unreachable | Public endpoint configuration did not match the replacement instance |

## Supporting Documents

- [Operational command reference](COMMAND-REF.md)
- [Reusable incident template](INCIDENT-TEMPLATE.md)
- [Security and publication policy](SECURITY.md)

## Architecture Context

```text
User
  ↓
DNS and TLS
  ↓
AWS Security Group
  ↓
NGINX
  ↓
Gunicorn
  ↓
Flask
  ↓
CloudWatch Logs and Metrics
  ↓
Python / AI-assisted incident analysis
```

## Evidence Standard

A report only marks recovery as successful when supported by evidence such as:

- `systemctl` service state
- `journalctl` entries
- NGINX access or error logs
- A listening-port check
- HTTP status validation
- CloudWatch log or alarm evidence
- DNS resolution
- Certificate validation
- Terraform validation or plan output

Commands that were useful for follow-up, but were not part of the captured terminal session, are labeled as additional validation commands.

## Security

All public examples use placeholders:

```text
[PUBLIC_IP]
[PRIVATE_IP]
[SSH_KEY]
[INSTANCE_ID]
[SECURITY_GROUP_ID]
[LOG_GROUP]
[AWS_REGION]
[DOMAIN]
```

No private keys, API keys, AWS account IDs, Terraform state, customer data, or real infrastructure identifiers should be committed.

## Suggested Repository Location

```text
cloud-support-platform/
└── incident-reports/
    ├── README.md
    ├── SECURITY.md
    ├── COMMAND-REFERENCE.md
    ├── INCIDENT-TEMPLATE.md
    ├── INC-001-ssh-private-ip-timeout.md
    ├── INC-002-nginx-permission-and-service-validation.md
    ├── INC-003-flask-gunicorn-backend-outage-502.md
    ├── INC-004-nginx-down-connection-refused.md
    ├── INC-005-nginx-restart-timeout.md
    ├── INC-006-cloudwatch-iam-and-ai-log-analysis.md
    └── INC-007-dns-https-and-ec2-migration-validation.md
```
