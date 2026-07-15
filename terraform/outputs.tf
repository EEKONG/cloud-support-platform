output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.web_server.id
}

output "elastic_ip" {
  description = "Elastic IP attached to the EC2 instance"
  value       = aws_eip.web_eip.public_ip
}

output "ssh_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh -i xxxxxxxxx.pem ec2-user@${aws_eip.web_eip.public_ip}"
}

output "website_http_url" {
  description = "HTTP URL"
  value       = "http://${aws_eip.web_eip.public_ip}"
}

output "website_https_url" {
  description = "HTTPS URL"
  value       = "https://${aws_eip.web_eip.public_ip}"
}
