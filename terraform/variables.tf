variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ca-central-1"

  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]+$", var.aws_region))
    error_message = "aws_region must be a valid AWS region name such as ca-central-1."
  }
}

variable "project_name" {
  description = "Project name used for AWS resource names and tags"
  type        = string
  default     = "cloud-support-platform"

  validation {
    condition     = can(regex("^[A-Za-z0-9][A-Za-z0-9-]{1,62}$", var.project_name))
    error_message = "project_name must be 2-63 characters and contain only letters, numbers, and hyphens."
  }
}

variable "ami_id" {
  description = "Custom AMI ID created from the existing EC2 instance"
  type        = string

  validation {
    condition     = can(regex("^ami-[0-9a-fA-F]+$", var.ami_id))
    error_message = "ami_id must be a valid AMI identifier such as ami-0123456789abcdef0."
  }
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"

  validation {
    condition     = can(regex("^[a-z][a-z0-9]*\\.[a-z0-9]+$", var.instance_type))
    error_message = "instance_type must be a valid EC2 instance type format such as t3.micro."
  }
}

variable "key_name" {
  description = "Existing AWS EC2 key pair name"
  type        = string

  validation {
    condition     = length(trimspace(var.key_name)) > 0
    error_message = "key_name must not be empty."
  }
}

variable "domain_name" {
  description = "Primary domain name used by the application"
  type        = string
  default     = "edikanekong.online"

  validation {
    condition = can(regex(
      "^([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\\.)+[a-zA-Z]{2,}$",
      var.domain_name
    ))
    error_message = "domain_name must be a valid domain name such as edikanekong.online."
  }
}