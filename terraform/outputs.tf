output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.web_server.id
}

output "elastic_ip" {
  description = "Elastic IP attached to the EC2 instance"
  value       = aws_eip.web_eip.public_ip
}

output "public_dns" {
  description = "Public DNS hostname associated with the Elastic IP"
  value       = aws_eip.web_eip.public_dns
}

output "application_url" {
  description = "Primary HTTPS URL for the application"
  value       = "https://${var.domain_name}"
}

output "session_manager_command" {
  description = "AWS CLI command for connecting through Session Manager"
  value       = "aws ssm start-session --target ${aws_instance.web_server.id} --region ${var.aws_region}"
}

output "website_http_url" {
  description = "HTTP URL that redirects to HTTPS"
  value       = "http://${var.domain_name}"
}

output "website_https_url" {
  description = "Primary HTTPS URL"
  value       = "https://${var.domain_name}"
}

output "www_https_url" {
  description = "HTTPS URL using the www subdomain"
  value       = "https://www.${var.domain_name}"
}

output "sns_topic_arn" {
  description = "SNS topic used by CloudWatch alarms"
  value       = aws_sns_topic.alerts.arn
}