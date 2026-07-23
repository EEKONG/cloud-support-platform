#!/bin/bash

set -euo pipefail

# Record bootstrap output for troubleshooting.
exec > >(tee /var/log/user-data.log | logger -t user-data -s 2>/dev/console) 2>&1

echo "Starting EC2 bootstrap..."

# Install the CloudWatch Agent.
dnf install -y amazon-cloudwatch-agent

# Start the application services already included in the current AMI.
systemctl enable --now nginx
systemctl enable --now flaskapp

# Ensure the NGINX log directory and files exist.
mkdir -p /var/log/nginx
touch /var/log/nginx/access.log
touch /var/log/nginx/error.log

# Create the CloudWatch Agent configuration.
mkdir -p /opt/aws/amazon-cloudwatch-agent/etc

cat > /opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-agent.json <<'EOF'
{
  "agent": {
    "run_as_user": "root"
  },
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/nginx/access.log",
            "log_group_name": "/ec2/flask-nginx/access",
            "log_stream_name": "{instance_id}",
            "timezone": "UTC"
          },
          {
            "file_path": "/var/log/nginx/error.log",
            "log_group_name": "/ec2/flask-nginx/error",
            "log_stream_name": "{instance_id}",
            "timezone": "UTC"
          }
        ]
      }
    }
  }
}
EOF

# Load the configuration and start the CloudWatch Agent.
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -s \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-agent.json

systemctl enable amazon-cloudwatch-agent

echo "EC2 bootstrap completed successfully."