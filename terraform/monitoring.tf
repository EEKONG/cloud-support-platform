# Allow the EC2 CloudWatch Agent to publish logs and metrics
resource "aws_iam_role_policy_attachment" "cloudwatch_agent" {
  role       = aws_iam_role.ec2_ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

# Existing NGINX log groups will be imported into Terraform
resource "aws_cloudwatch_log_group" "nginx_access" {
  name              = "/ec2/flask-nginx/access"
  retention_in_days = 14

  tags = {
    Name    = "${var.project_name}-nginx-access"
    Project = var.project_name
  }
}

resource "aws_cloudwatch_log_group" "nginx_error" {
  name              = "/ec2/flask-nginx/error"
  retention_in_days = 14

  tags = {
    Name    = "${var.project_name}-nginx-error"
    Project = var.project_name
  }
}

# Dedicated notification topic for this project
resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-alerts"

  tags = {
    Name    = "${var.project_name}-alerts"
    Project = var.project_name
  }
}

# Native EC2 CPU alarm
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${var.project_name}-high-cpu"
  alarm_description   = "EC2 CPU utilization is at least 80 percent for 10 minutes."
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  datapoints_to_alarm = 2
  threshold           = 80
  period              = 300
  namespace           = "AWS/EC2"
  metric_name         = "CPUUtilization"
  statistic           = "Average"
  treat_missing_data  = "missing"
  actions_enabled     = true

  dimensions = {
    InstanceId = aws_instance.web_server.id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]

  tags = {
    Name    = "${var.project_name}-high-cpu"
    Project = var.project_name
  }
}

# Alarm when either the EC2 system or instance status check fails
resource "aws_cloudwatch_metric_alarm" "status_check_failed" {
  alarm_name          = "${var.project_name}-status-check-failed"
  alarm_description   = "EC2 system or instance status check has failed."
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  datapoints_to_alarm = 2
  threshold           = 1
  period              = 60
  namespace           = "AWS/EC2"
  metric_name         = "StatusCheckFailed"
  statistic           = "Maximum"
  treat_missing_data  = "missing"
  actions_enabled     = true

  dimensions = {
    InstanceId = aws_instance.web_server.id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]

  tags = {
    Name    = "${var.project_name}-status-check-failed"
    Project = var.project_name
  }
}