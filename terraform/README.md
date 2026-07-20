# Terraform

This directory provisions the AWS infrastructure for the Cloud Support Platform lab:

- An EC2 security group allowing public HTTP and HTTPS access
- An EC2 instance created from an existing AMI
- An Elastic IP associated with the EC2 instance
- Instance bootstrap through `user_data.sh`
- An EC2 IAM role and instance profile
- AWS Systems Manager Session Manager access using `AmazonSSMManagedInstanceCore`

Administrative access is provided through AWS Systems Manager Session Manager. The security group does not expose inbound SSH on TCP port 22.

## Security Architecture

The EC2 instance uses a dedicated IAM role with an EC2 trust policy. The AWS-managed `AmazonSSMManagedInstanceCore` policy supplies the permissions required for the SSM Agent to communicate with Systems Manager.

The IAM role is attached to the EC2 instance through an instance profile.

The security group permits:

- HTTP on TCP port 80 from the internet
- HTTPS on TCP port 443 from the internet
- Outbound traffic required by the instance and SSM Agent
- No inbound SSH access

The existing EC2 key pair remains associated with the current instance because removing `key_name` could trigger instance replacement. However, the key pair cannot be used for inbound SSH while port 22 remains blocked.

## Prerequisites

- Terraform 1.6 or later
- AWS credentials configured outside this repository
- AWS permission to manage EC2, security groups, Elastic IPs, IAM roles, IAM instance profiles and policy attachments
- Permission to start AWS Systems Manager sessions
- An existing AMI in the selected AWS region
- An active Amazon SSM Agent on the AMI
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

You can also connect through:

1. AWS Console
2. EC2
3. Instances
4. Select the Terraform-managed instance
5. Connect
6. Session Manager
7. Connect

## Expected Outputs

- `instance_id`: Terraform-managed EC2 instance ID
- `elastic_ip`: Elastic IP associated with the instance
- `public_dns`: Public EC2 DNS name
- `application_url`: Primary HTTP application URL
- `website_http_url`: Public HTTP URL
- `website_https_url`: Public HTTPS URL
- `session_manager_command`: AWS CLI command for secure administrative access

## Validation Results

Validated on July 20, 2026:

- Terraform created the IAM role, policy attachment and instance profile.
- The instance profile was attached without replacing the EC2 instance.
- A new Session Manager shell opened successfully.
- The session operated as `ssm-user`.
- The Amazon SSM Agent reported `active`.
- External TCP connections to port 22 failed.
- External TCP connections to ports 80 and 443 succeeded.
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

`terraform destroy` deletes real AWS resources. Do not run it against infrastructure you still need.