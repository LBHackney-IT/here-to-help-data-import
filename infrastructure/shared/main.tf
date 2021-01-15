variable "function_name" {
  default = "here-to-help-data-ingestion"
}

variable "handler" {
  default = "lib.main.lambda_handler"
}

variable "runtime" {
  default = "python3.7"
}
variable "subnet_ids_for_lambda" {
  default = { "development" =  ["subnet-0deabb5d8fb9c3446", "subnet-000b89c249f12a8ad"],
              "staging" = ["subnet-06d3de1bd9181b0d7", "subnet-0ed7d7713d1127656"],
              "production" = ["subnet-01d3657f97a243261", "subnet-0b7b8fea07efabf34"]
            }
}
variable "sg_for_lambda" {
  default = { "development" =  ["sg-0295c6df4beffa609"],
              "staging" = ["sg-0cd6d0dd6097bb9e8"],
              "production" = ["sg-0e3ca1352f142d8c8"]
            }
}

variable "api_url" {
  type = string
}

variable "stage" {
  type = string
}

data "aws_ssm_parameter" "api_key" {
  name = "/cv-19-res-support-v3/${var.stage}/api-key"
}

data "aws_ssm_parameter" "gdrive_key" {
  name = "/cv-19-res-support-v3/${var.stage}/gdrive_key"
}

resource "local_file" "key_file" {
    content  = data.aws_ssm_parameter.gdrive_key.value
    filename = "../../lib_src/lib/key_file.json"
}

data "archive_file" "lib_zip_file" {
  type        = "zip"
  source_dir = "../../lib_src"
  output_path = "../../lambda.zip"

  depends_on = [
    data.local_file.key_file
  ]
}

resource "aws_s3_bucket" "s3_deployment_artefacts" {
  bucket        = "here-to-help-data-ingestion-${var.stage}"
  acl           = "private"
  force_destroy = true
}

resource "aws_s3_bucket_object" "handler" {
  bucket = aws_s3_bucket.s3_deployment_artefacts.bucket
  key    = "here-to-help-lambda-handler.zip"
  source = data.archive_file.lib_zip_file.output_path
  acl    = "private"
  etag   = filemd5(data.archive_file.lib_zip_file.output_path)

  depends_on = [
    data.archive_file.lib_zip_file
  ]
}

resource "aws_lambda_function" "here-to-help-lambda" {
  role             = aws_iam_role.here_to_help_role.arn
  handler          = var.handler
  runtime          = var.runtime
  function_name    = var.function_name
  s3_bucket        = aws_s3_bucket.s3_deployment_artefacts.bucket
  s3_key           = aws_s3_bucket_object.handler.key
  source_code_hash = data.archive_file.lib_zip_file.output_base64sha256
  timeout = 900

  vpc_config {
    subnet_ids         = lookup(var.subnet_ids_for_lambda, var.stage)
    security_group_ids = lookup(var.sg_for_lambda, var.stage)
  }
  environment {
    variables = {
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_URL = var.api_url
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_API_KEY = data.aws_ssm_parameter.api_key.value
    }
  }
   depends_on = [
    aws_s3_bucket_object.handler
  ]
}

# See also the following AWS managed policy: AWSLambdaBasicExecutionRole

resource "aws_cloudwatch_event_rule" "here-to-help-scheduled-event" {
  name                = "here-to-help-scheduled-event"
  description         = "Fires every one minutes"
  schedule_expression = "rate(1 hour)"
  is_enabled = false
}

resource "aws_cloudwatch_event_target" "check_google_sheet" {
  rule      = aws_cloudwatch_event_rule.here-to-help-scheduled-event.name
  target_id = "here-to-help-lambda"
  arn       = aws_lambda_function.here-to-help-lambda.arn
}

resource "aws_lambda_permission" "allow_lambda_logging_and_call_check_google_sheet" {
  statement_id_prefix  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.here-to-help-lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.here-to-help-scheduled-event.arn
}

resource "aws_iam_role" "here_to_help_role" {
  name               = "here-to-help-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.here_to_help_role.json
}

data "aws_iam_policy_document" "here_to_help_role" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "here_to_help_lambda_policy" {
    name        = "here-to-help-lambda-policy"
    policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:DescribeNetworkInterfaces",
        "ec2:CreateNetworkInterface",
        "ec2:DeleteNetworkInterface",
        "ec2:DescribeInstances",
        "ec2:AttachNetworkInterface"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "here-to-help-lambda-role-attachment" {
  role       = aws_iam_role.here_to_help_role.name
  policy_arn = aws_iam_policy.here_to_help_lambda_policy.arn
}
