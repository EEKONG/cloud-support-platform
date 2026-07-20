# Terraform

This directory provisions and manages AWS infrastructure for the Cloud Support Platform lab:

- An EC2 security group allowing public HTTP and HTTPS access
- An EC2 instance created from an existing AMI
- An Elastic IP associated with the EC2 instance
- Instance bootstrap through `user_data.sh`
- An EC2 IAM role and instance profile
- AWS Systems Manager Session Manager access
- Amazon CloudWatch Agent permissions
- NGINX access and error log groups
- CPU and EC2 status-check alarms
- An SNS topic for alarm notifications

Administrative access is provided through AWS Systems Manager Session Manager. The security group does not expose inbound SSH on TCP port 22.

## Security Architecture

The EC2 instance uses a dedicated IAM role with an EC2 trust policy. The role has the following AWS-managed policies:

- `AmazonSSMManagedInstanceCore` for Systems Manager access
- `CloudWatchAgentServerPolicy` for publishing CloudWatch logs and metrics

The IAM role is attached to the EC2 instance through an instance profile.

The security group permits:

- HTTP on TCP port 80 from the internet
- HTTPS on TCP port 443 from the internet
- Outbound traffic required by the instance, SSM Agent and CloudWatch Agent
- No inbound SSH access

The existing EC2 key pair remains associated with the current instance because removing `key_name` could trigger instance replacement. However, the key pair cannot be used for direct inbound SSH while port 22 remains blocked by the security group.

## Prerequisites

- Terraform 1.6 or later
- AWS credentials configured outside this repository
- AWS permission to manage EC2, security groups and Elastic IPs
- AWS permission to manage IAM roles, instance profiles and policy attachments
- AWS permission to manage CloudWatch, CloudWatch Logs and SNS
- Permission to start AWS Systems Manager sessions
- An existing AMI in the selected AWS region
- An active Amazon SSM Agent on the AMI
- An active Amazon CloudWatch Agent on the AMI
- An existing EC2 key pair for the current configuration
- AWS CLI and Session Manager plugin when connecting from the command line

The AWS Console can also be used to start a Session Manager connection.

Do not commit AWS credentials, private keys, `terraform.tfvars`, `.terraform/`, Terraform plan files or Terraform state files.

## Variables

| Name | Required | Description | Example |
|---|---:|---|---|
| `aws_region` | No | AWS region where resources are created. | `ca-central-1` |
| `project_name` | No | Name used for resource names and tags. | `cloud-support-platform` |
| `ami_id` | Yes | Existing AMI used to create the EC2 instance. | `ami-0123456789abcdef0` |
| `instance_type` | No | EC2 instance type. | `t3.micro` |
| `key_name` | Yes | Existing key pair associated with the current EC2 instance. | `your-existing-key-pair` |

## Local Configuration

Create a local `terraform.tfvars` file from the safe example.

PowerShell:

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
```

Bash:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your local values. The real file is ignored by Git and must not be committed.

## Terraform Commands

Run these commands from this directory:

```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan
```

Review the plan carefully before applying:

```bash
terraform apply
```

Terraform operations can create chargeable AWS resources.

## Connecting Through Session Manager

Display the generated Session Manager command:

```bash
terraform output -raw session_manager_command
```

The generated command follows this format:

```bash
aws ssm start-session \
  --target <instance-id> \
  --region ca-central-1
```

You can also connect through the AWS Console:

1. Open EC2.
2. Select **Instances**.
3. Select the Terraform-managed instance.
4. Choose **Connect**.
5. Select **Session Manager**.
6. Choose **Connect**.

## Monitoring and Alerting

### CloudWatch Agent

The EC2 IAM role includes `CloudWatchAgentServerPolicy`, allowing the CloudWatch Agent to publish logs and custom metrics.

The current AMI already contains the CloudWatch Agent and its configuration. The existing `user_data.sh` starts NGINX and the Flask application but does not install or configure the CloudWatch Agent.

This is a known limitation: a future AMI or deployment must either include the existing agent configuration or add CloudWatch Agent installation and configuration to the bootstrap process.

### Log Collection

| Local log | CloudWatch log group | Retention |
|---|---|---:|
| `/var/log/nginx/access.log` | `/ec2/flask-nginx/access` | 14 days |
| `/var/log/nginx/error.log` | `/ec2/flask-nginx/error` | 14 days |

The log groups existed before the Terraform monitoring implementation. They were imported into Terraform state rather than recreated.

Log streams use the EC2 instance ID, allowing events from the original and Terraform-managed instances to remain distinguishable.

### CloudWatch Alarms

| Alarm | Metric | Condition |
|---|---|---|
| `cloud-support-platform-high-cpu` | `AWS/EC2 CPUUtilization` | Average CPU at or above 80% for two consecutive five-minute periods |
| `cloud-support-platform-status-check-failed` | `AWS/EC2 StatusCheckFailed` | Maximum value of 1 for two consecutive one-minute periods |

Both alarms send SNS notifications when entering `ALARM` and when recovering to `OK`.

The alarms are notification-only. They do not automatically reboot, stop, recover or terminate the EC2 instance.

### SNS Notifications

Terraform manages the dedicated SNS topic:

```text
cloud-support-platform-alerts
```

Display its ARN with:

```bash
terraform output -raw sns_topic_arn
```

Email subscriptions are created and confirmed separately because Amazon SNS requires the recipient to approve email delivery. The recipient’s email address is not stored in the repository.

### Legacy Monitoring Resources

The older `tse-*` CloudWatch alarms and `Default_CloudWatch_Alarms_Topic` were created outside this Terraform configuration. They remain associated with the original manually created environment and are not managed or deleted by this project.

They should be reviewed during the planned migration from the original EC2 instance.

## Expected Outputs

- `instance_id`: Terraform-managed EC2 instance ID
- `elastic_ip`: Elastic IP associated with the instance
- `public_dns`: Public EC2 DNS name
- `application_url`: Primary HTTP application URL
- `website_http_url`: Public HTTP URL
- `website_https_url`: Public HTTPS URL
- `session_manager_command`: AWS CLI command for secure administrative access
- `sns_topic_arn`: SNS topic used for CloudWatch alarm notifications

## Validation Results

Validated on July 20, 2026.

### Secure Administrative Access

- Terraform created the IAM role, SSM policy attachment and instance profile.
- The instance profile was attached without replacing the EC2 instance.
- A new Session Manager shell opened successfully.
- The session operated as `ssm-user`.
- The Amazon SSM Agent reported `active`.
- External TCP connections to port 22 failed.
- External TCP connections to ports 80 and 443 succeeded.

### Monitoring and Alerting

- The Amazon CloudWatch Agent reported `active` and `running`.
- Access and error log streams appeared for the Terraform-managed instance.
- Both imported log groups were configured with 14-day retention.
- The CPU and status-check alarms reached a healthy `OK` state.
- The SNS email subscription was confirmed.
- A controlled test changed the CPU alarm from `OK` to `ALARM` and back to `OK`.
- Both alarm and recovery emails were delivered.
- CloudWatch recorded the complete `INSUFFICIENT_DATA → OK → ALARM → OK` state history.
- `terraform plan` reported no configuration drift.

## Cleanup

When the lab infrastructure is no longer needed, review the destruction plan first:

```bash
terraform plan -destroy
```

Only after confirming that all targeted resources can be removed should you run:

```bash
terraform destroy
```

Because the NGINX log groups are now managed by Terraform, `terraform destroy` will delete those log groups and their stored events. Export any logs that must be retained before destroying the infrastructure.

The legacy `tse-*` alarms, original EC2 instance and `Default_CloudWatch_Alarms_Topic` are outside this Terraform state and require separate review.

Do not run `terraform destroy` against infrastructure you still need.