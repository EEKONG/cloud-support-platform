# Security and Publication Policy

This folder is intended for public GitHub use.

## Never Commit

- Private keys or `.pem` files
- `.env` files
- OpenAI or other API keys
- AWS access keys, secret keys, or session tokens
- AWS account IDs
- Terraform state or plan files
- Real customer data
- Internal tickets or customer communications
- Unredacted public IPs, private IPs, hostnames, or SSH fingerprints

## Required Placeholders

Use:

```text
[PUBLIC_IP]
[PRIVATE_IP]
[SSH_KEY]
[INSTANCE_ID]
[SECURITY_GROUP_ID]
[LOG_GROUP]
[LOG_STREAM]
[AWS_REGION]
[DOMAIN]
```

Loopback addresses such as `127.0.0.1` and non-secret network ranges used for technical explanation are acceptable.

## Pre-Commit Review

Run:

```bash
git diff --cached
```

Search for common secret patterns:

```bash
git grep -n -E "(AKIA|ASIA|BEGIN.*PRIVATE KEY|aws_secret_access_key|OPENAI_API_KEY=)"
```

Search staged files for likely IPv4 addresses, then manually verify that only loopback, documentation ranges, or approved placeholders remain:

```bash
git diff --cached | grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}'
```

Inspect ignored files:

```bash
git status --ignored
```

## Honesty Standard

These documents describe a personal AWS lab. Use language such as:

- controlled incident simulation
- production-style support lab
- simulated user impact
- example customer update

Do not imply that a lab exercise was a real customer outage.