# Security Group
resource "aws_security_group" "web_sg" {
  name        = "${var.project_name}-sg"
  description = "Security group for Flask NGINX Support App"

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${var.project_name}-security-group"
    Project = var.project_name
  }
}

# EC2 Instance
resource "aws_instance" "web_server" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = var.key_name
  iam_instance_profile        = aws_iam_instance_profile.ec2_ssm_profile.name
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true

  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name    = "${var.project_name}-ec2"
    Project = var.project_name
  }
}

# Elastic IP
resource "aws_eip" "web_eip" {
  instance = aws_instance.web_server.id
  domain   = "vpc"

  tags = {
    Name    = "${var.project_name}-eip"
    Project = var.project_name
  }
}
