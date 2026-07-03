variable "aws_region" {
  default     = "eu-west-1"
  description = "AWS region"
}

variable "app_name" {
  default     = "ecs-test"
  description = "Application name used for resource naming"
}

variable "container_port" {
  default     = 5000
  description = "Container port the Flask app listens on"
}

variable "cpu" {
  default     = 256
  description = "ECS task CPU units (0.25 vCPU)"
}

variable "memory" {
  default     = 512
  description = "ECS task memory in MB"
}

variable "desired_count" {
  default     = 1
  description = "Number of ECS tasks to run"
}
