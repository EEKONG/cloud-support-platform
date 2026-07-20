output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.web_server.id
}

output "elastic_ip" {
  description = "Elastic IP attached to the EC2 instance"
  value       = aws_eip.web_eip.public_ip
}

output "public_dns" {
  description = "Public DNS name for the Elastic IP"
  value       = aws_eip.web_eip.public_dns
}

output "application_url" {
  description = "Primary HTTP URL for the application"
  value       = "http://${aws_eip.web_eip.public_ip}"
}

output "session_manager_command" {
  description = "AWS CLI command for connecting through Session Manager"
  value       = "aws ssm start-session --target ${aws_instance.web_server.id} --region ${var.aws_region}"
}

output "website_http_url" {
  description = "HTTP URL"
  value       = "http://${aws_eip.web_eip.public_ip}"
}

output "website_https_url" {
  description = "HTTPS URL"
  value       = "https://${aws_eip.web_eip.public_ip}"
}