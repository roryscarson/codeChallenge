terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  version = "~> 2.38"
  region  = var.aws_region
}
