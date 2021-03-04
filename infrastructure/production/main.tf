terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }

 backend "s3" {
    region     = "eu-west-2"
    key        = "tf-remote-state/here-to-help-data-ingestion"
    bucket     = "here-to-help-data-ingestion-terraform-state-production"
    encrypt    = true
  }
}

provider "aws" {
  region = "eu-west-2"
}

variable "api_url" {
  type = string
}
variable "email_addresses" {
  type = string
}
module "all-resources" {
  source = "../shared"
  stage = "production"
  api_url = var.api_url
  email_addresses = var.email_addresses
}
