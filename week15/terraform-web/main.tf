provider "aws" {
  region  = var.region
  version = ">= 5.0"
}

data "aws_availability_zones" "available" {}

# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = ">= 5.0"

  name     = "advscripting"
  cidr     = var.cidr

  azs = data.aws_availability_zones.available.names

  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets

  enable_nat_gateway = false
  single_nat_gateway = false
  enable_vpn_gateway = false

  map_public_ip_on_launch = true

}

# Security Group Module for application servers
module "web_server_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = ">= 5.0"

  name        = "web-sg"
  description = "Security group for web servers"
  vpc_id      = module.vpc.vpc_id

  ingress_with_cidr_blocks = [
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      description = "Allow all traffic on port 80"
      cidr_blocks = "0.0.0.0/0"
    },
  ]
}

output "security_group_id" {
  value = module.web_server_sg.security_group_id
}

# AMI Data Element
data "aws_ami" "web_ami" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  owners = ["amazon"]
}

# EC2 Instance Module
module "web_server" {
  source = "terraform-aws-modules/ec2-instance/aws"

  name               = "haene-web-server"
  ami                = data.aws_ami.web_ami.id
  instance_type      = "t2.micro"
  subnet_id          = module.vpc.public_subnets[0]
  key_name           = "vockey"

  vpc_security_group_ids = [module.web_server_sg.security_group_id]
  user_data = templatefile("${path.module}/init-script.sh", {
    file_content = "HaeneSafavi"
  })
}

# Output for web server's public IP address
output "web_server_public_ip" {
  value = module.web_server.public_ip
}