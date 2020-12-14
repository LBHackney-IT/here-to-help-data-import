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
    bucket     = "here-to-help-data-ingestion-terraform-state"
    encrypt    = true
  }
}

provider "aws" {
  region = "eu-west-2"
}

module "all-resources" {
  source = "../shared"
  stage = "development"
}
