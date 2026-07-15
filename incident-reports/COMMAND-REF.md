# Cloud Support Platform — Operational Command Reference

This document consolidates the commands used or documented during the project.

## Important Safety Notes

- Replace all placeholders before running commands.
- Never commit keys, `.env`, credentials, or Terraform state.
- Use destructive commands such as `pkill` and `systemctl stop` only in an authorized lab or maintenance window.
- Capture evidence before restarting services.
- Prefer `reload` over `restart` for validated NGINX configuration changes.

---

# 1. Windows Network and SSH Commands

## Test reachability

```powershell
ping [PRIVATE_IP]
ping [PUBLIC_IP]
```

## Move to the key directory

```powershell
cd Downloads
dir
```

## SSH with a key

```powershell
ssh -i [SSH_KEY] ec2-user@[PUBLIC_IP]
```

## Verbose SSH troubleshooting

```powershell
ssh -vvv -i [SSH_KEY] ec2-user@[PUBLIC_IP]
```

## Test TCP 22

```powershell
Test-NetConnection [PUBLIC_IP] -Port 22
```

---

# 2. Linux Navigation and File Inspection

```bash
pwd
ls
ls -la
cd /home/ec2-user
cd /home/ec2-user/flask-support-app
cd /var/log
cd /var/log/nginx
cat app.py
nano app.py
sudo nano /etc/nginx/nginx.conf
```

---

# 3. Host and Network Validation

## Local and private-address tests

```bash
ping localhost
ping [PRIVATE_IP]
ping [PUBLIC_IP]
```

## Current public IP

```bash
curl https://checkip.amazonaws.com
```

## Listening ports

```bash
sudo ss -lntp
sudo ss -lntp | grep -E ':80|:443|:5000'
```

Alternatives:

```bash
sudo netstat -lntp
sudo lsof -iTCP -sTCP:LISTEN
```

## DNS

```bash
dig +short [DOMAIN]
dig +short www.[DOMAIN]
nslookup [DOMAIN]
```

---

# 4. NGINX Service Management

## Commands originally attempted without sudo

```bash
systemctl enable nginx
systemctl start nginx
```

These returned `Access denied`.

## Correct privileged commands

```bash
sudo systemctl status nginx
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx
sudo systemctl enable nginx
sudo systemctl enable --now nginx
sudo systemctl is-active nginx
sudo systemctl is-enabled nginx
```

## Configuration validation

```bash
sudo nginx -t
sudo nginx -T
```

## Safe reload pattern

```bash
sudo nginx -t && sudo systemctl reload nginx
```

## Service definition and timeout settings

```bash
systemctl cat nginx
systemctl show nginx -p TimeoutStopUSec
```

---

# 5. NGINX Logs

## Systemd journal

```bash
sudo journalctl -u nginx
sudo journalctl -u nginx -n 50 --no-pager
sudo journalctl -u nginx --since "30 minutes ago"
```

## Access and error logs

```bash
sudo tail -n 50 /var/log/nginx/access.log
sudo tail -n 50 /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Search for failures

```bash
sudo grep -i "error" /var/log/nginx/error.log
sudo grep " 502 " /var/log/nginx/access.log
sudo grep "connect() failed" /var/log/nginx/error.log
```

## Find duplicate server names

```bash
sudo grep -R "server_name _" /etc/nginx /etc/nginx/conf.d
sudo grep -R "server_name" /etc/nginx /etc/nginx/conf.d
```

---

# 6. HTTP and Reverse-Proxy Testing

## Test NGINX

```bash
curl localhost
curl localhost:80
curl -I localhost
curl -I http://localhost
```

## Test the backend directly

```bash
curl localhost:5000
curl -I http://127.0.0.1:5000
```

## Test the domain

```bash
curl -I http://[DOMAIN]
curl -I https://[DOMAIN]
curl -Ik https://[DOMAIN]
```

## Interpretation

```text
HTTP 200              = request succeeded
HTTP 301/302          = redirect
HTTP 400              = bad request
HTTP 401/403          = authentication/authorization
HTTP 404              = route or resource missing
HTTP 500              = application error
HTTP 502              = proxy cannot reach a valid backend
HTTP 504              = upstream timed out
Connection refused    = no listener on the target port
Connection timed out  = traffic did not complete the connection
```

---

# 7. Flask Development-Server Commands

## Start the Flask application manually

```bash
python3 app.py
```

Observed bind addresses:

```text
http://127.0.0.1:5000
http://[PRIVATE_IP]:5000
```

The Flask development server is for testing only. The project later used Gunicorn behind NGINX.

## Common working-directory failure

Running from `/` produced:

```bash
python3 app.py
```

```text
python3: can't open file '//app.py': No such file or directory
```

Correct approach:

```bash
cd /home/ec2-user
python3 app.py
```

or use the systemd/Gunicorn service.

---

# 8. Process Investigation and Failure Simulation

## Find Python processes

```bash
ps aux | grep python
ps aux | grep '[p]ython'
pgrep -a python
```

## Find Gunicorn

```bash
ps aux | grep gunicorn
pgrep -a gunicorn
```

## Lab-only termination commands

```bash
pkill python
pkill -f app.py
```

These commands were used to simulate an application outage. They should not be used casually in production because they may terminate unrelated processes.

---

# 9. Flask/Gunicorn systemd Service

```bash
sudo systemctl status flaskapp
sudo systemctl start flaskapp
sudo systemctl stop flaskapp
sudo systemctl restart flaskapp
sudo systemctl enable flaskapp
sudo systemctl is-active flaskapp
```

## Logs

```bash
sudo journalctl -u flaskapp
sudo journalctl -u flaskapp -n 20 --no-pager
sudo journalctl -u flaskapp --since "30 minutes ago"
```

## Expected Gunicorn startup evidence

```text
Starting gunicorn
Listening at: http://127.0.0.1:5000
Booting worker with pid
```

---

# 10. Linux Service Discovery

```bash
systemctl list-units --type=service
systemctl list-unit-files --type=service
```

Relevant services included:

```text
nginx.service
sshd.service
amazon-ssm-agent.service
flaskapp.service
```

---

# 11. Firewall and AWS Security Boundary

The following command was tested:

```bash
sudo firewall-cmd --list-all
```

Observed:

```text
firewall-cmd: command not found
```

This indicated that `firewalld` was not installed or used. Network access was primarily controlled through AWS security groups.

Additional checks:

```bash
sudo nft list ruleset
sudo iptables -L -n -v
```

AWS:

```bash
aws ec2 describe-security-groups \
  --group-ids [SECURITY_GROUP_ID] \
  --region [AWS_REGION]
```

---

# 12. CloudWatch Agent

```bash
sudo systemctl status amazon-cloudwatch-agent
sudo systemctl restart amazon-cloudwatch-agent
sudo journalctl -u amazon-cloudwatch-agent -n 100 --no-pager
```

Agent control:

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status
```

Configuration:

```bash
sudo cat /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
```

---

# 13. AWS and CloudWatch Logs

## Confirm identity

```bash
aws sts get-caller-identity
```

## Log groups and streams

```bash
aws logs describe-log-groups --region [AWS_REGION]
```

```bash
aws logs describe-log-streams \
  --log-group-name [LOG_GROUP] \
  --order-by LastEventTime \
  --descending \
  --region [AWS_REGION]
```

## Retrieve events

```bash
aws logs get-log-events \
  --log-group-name [LOG_GROUP] \
  --log-stream-name [LOG_STREAM] \
  --region [AWS_REGION]
```

```bash
aws logs filter-log-events \
  --log-group-name [LOG_GROUP] \
  --region [AWS_REGION]
```

Required permission:

```text
logs:FilterLogEvents
```

---

# 14. AI Log Analysis

## Check configuration without printing the secret

```bash
test -n "$OPENAI_API_KEY" && echo "OPENAI_API_KEY is set" || echo "OPENAI_API_KEY is missing"
```

## Set for current Linux shell

```bash
export OPENAI_API_KEY="[REDACTED]"
```

## PowerShell

```powershell
$env:OPENAI_API_KEY="[REDACTED]"
```

## Run analysis

```bash
python3 analyze_logs.py
```

or:

```bash
python3 ai-log-intelligence/analyze_logs.py
```

---

# 15. SSL/TLS and Certbot

```bash
sudo certbot certificates
sudo certbot renew --dry-run
sudo nginx -t
sudo systemctl reload nginx
```

External certificate inspection:

```bash
openssl s_client \
  -connect [DOMAIN]:443 \
  -servername [DOMAIN]
```

Certificate dates only:

```bash
echo | openssl s_client \
  -connect [DOMAIN]:443 \
  -servername [DOMAIN] 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer
```

---

# 16. System Resources and Load Testing

## Memory and disk

```bash
free -h
df -h
du -sh /var/log/*
```

## CPU and process activity

```bash
top
ps aux --sort=-%cpu | head
ps aux --sort=-%mem | head
```

## Controlled lab load

```bash
stress --cpu 1 --timeout 300
```

Memory load should be carefully sized to the instance. Do not exhaust all memory on a production host.

---

# 17. Terraform

```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan
terraform apply
terraform output
terraform state list
terraform show
```

Security:

```text
Do not commit:
terraform.tfstate
terraform.tfstate.*
.terraform/
*.tfvars
*.pem
.env
```

---

# 18. Git Evidence

```bash
git status
git diff
git add .
git commit -m "docs: add incident reports and command reference"
git log --oneline -5
```

Before commit:

```bash
git grep -n -E "(AKIA|BEGIN.*PRIVATE KEY|OPENAI_API_KEY=|aws_secret_access_key)"
```