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

variable "function_name" {
  default = "here-to-help-data-ingestion"
}

variable "role" {
  default = {"development" = "arn:aws:iam::859159924354:role/cv-19-res-support-dev-eu-west-2-lambdaRole"}
}

variable "handler" {
  default = "lib.main.lambda_handler"
}

variable "runtime" {
  default = "python3.7"
}
variable "subnet_ids_for_lambda" {
  default = {"development" =  ["subnet-0deabb5d8fb9c3446", "subnet-000b89c249f12a8ad"]}
}
variable "sg_for_lambda" {
  default = {"development" =  ["sg-0295c6df4beffa609"]}
}

variable "stage" {
  type = string
}


data "local_file" "here-to-help-lambda-object" {
  filename = "../lambda.zip"
}

resource "aws_s3_bucket" "s3_deployment_artefacts" {
  bucket        = "here-to-help-data-ingestion-dev"
  acl           = "private"
  force_destroy = true
}

resource "aws_s3_bucket_object" "handler" {
  bucket = aws_s3_bucket.s3_deployment_artefacts.bucket
  key    = "handler-${filebase64sha256(data.local_file.here-to-help-lambda-object.filename)}.zip"
  source = data.local_file.here-to-help-lambda-object.filename
  acl    = "private"
}

resource "aws_lambda_function" "here-to-help-lambda" {
  role             = lookup(var.role, var.stage)
  handler          = var.handler
  runtime          = var.runtime
  function_name    = var.function_name
  s3_bucket        = aws_s3_bucket.s3_deployment_artefacts.bucket
  s3_key           = aws_s3_bucket_object.handler.key

  vpc_config {
    subnet_ids         = lookup(var.subnet_ids_for_lambda, var.stage)
    security_group_ids = lookup(var.sg_for_lambda, var.stage)
  }
}

//resource "aws_iam_role" "here_to_help_role" {
//  name               = "here-to-help-lambda-role"
//  assume_role_policy = data.aws_iam_policy_document.here_to_help_role.json
//}
//
//data "aws_iam_policy_document" "here_to_help_role" {
//  statement {
//    actions = ["sts:AssumeRole"]
//    effect  = "Allow"
//
//    principals {
//      type        = "Service"
//      identifiers = ["lambda.amazonaws.com"]
//    }
//  }
//}