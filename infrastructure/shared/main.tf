variable "function_name" {
  default = "here-to-help-data-ingestion"
}

variable "NSSS_function_name" {
  default = "here-to-help-data-ingestion-NSSS"
}

variable "SPL_function_name" {
  default = "here-to-help-data-ingestion-SPL"
}

variable "self_isolation_function_name" {
  default = "here-to-help-data-ingestion-self-isolation"
}

variable "generic_ingestion_function_name" {
  default = "here-to-help-data-generic-ingestion"
}

variable "data_ingestion_function_names" {
  default = ["here-to-help-data-ingestion","here-to-help-data-ingestion-NSSS", "here-to-help-data-ingestion-SPL", "here-to-help-data-ingestion-self-isolation", "here-to-help-data-generic-ingestion"]
}

variable "generic_ingestion_handler" {
  default = "lib.main.generic_ingestion_lambda_handler"
}

variable "self_isolation_handler" {
  default = "lib.main.self_isolation_lambda_handler"
}

variable "spl_handler" {
  default = "lib.main.spl_lambda_handler"
}

variable "nsss_handler" {
  default = "lib.main.nsss_lambda_handler"
}

variable "handler" {
  default = "lib.main.lambda_handler"
}

variable "runtime" {
  default = "python3.8"
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

locals {
  emails = split(",", data.aws_ssm_parameter.email-addresses-for-sns.value)
}

variable "stage" {
  type = string
}

data "aws_ssm_parameter" "email-addresses-for-sns" {
  name = "/here-to-help-data-ingestion/${var.stage}/email-addresses-for-sns"
}

data "aws_ssm_parameter" "api_key" {
  name = "/cv-19-res-support-v3/${var.stage}/api-key"
}

data "aws_ssm_parameter" "api_base_url" {
  name = "/cv-19-res-support-v3/${var.stage}/api-base-url"
}

data "aws_ssm_parameter" "ct_inbound_folder_id" {
  name = "/cv-19-res-support-v3/${var.stage}/ct_inbound_folder_id"
}

data "aws_ssm_parameter" "ct_outbound_folder_id" {
  name = "/cv-19-res-support-v3/${var.stage}/ct_outbound_folder_id"
}

data "aws_ssm_parameter" "cev_inbound_folder_id" {
  name = "/cv-19-res-support-v3/${var.stage}/cev_inbound_folder_id"
}

data "aws_ssm_parameter" "cev_outbound_folder_id" {
  name = "/cv-19-res-support-v3/${var.stage}/cev_outbound_folder_id"
}

data "aws_ssm_parameter" "spl_inbound_folder_id" {
  name = "/cv-19-res-support-v3/${var.stage}/spl_inbound_folder_id"
}

data "aws_ssm_parameter" "spl_outbound_folder_id" {
  name = "/cv-19-res-support-v3/${var.stage}/spl_outbound_folder_id"
}

data "aws_ssm_parameter" "self_isolation_inbound_folder_id" {
  name = "/cv-19-res-support-v3/${var.stage}/self_isolation_inbound_folder_id"
}

data "aws_ssm_parameter" "self_isolation_outbound_folder_id" {
  name = "/cv-19-res-support-v3/${var.stage}/self_isolation_outbound_folder_id"
}

data "aws_ssm_parameter" "generic_ingestion_inbound_folder_id" {
  name = "/cv-19-res-support-v3/${var.stage}/generic_ingestion_inbound_folder_id"
}

data "aws_ssm_parameter" "generic_ingestion_outbound_folder_id" {
  name = "/cv-19-res-support-v3/${var.stage}/generic_ingestion_outbound_folder_id"
}

data "aws_ssm_parameter" "excluded_ctas_ids" {
  name = "/cv-19-res-support-v3/${var.stage}/excluded_ctas_ids"
}

data "archive_file" "lib_zip_file" {
  type        = "zip"
  source_dir = "../../lib_src"
  output_path = "../../lambda.zip"
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
  memory_size = 10240
  timeout = 900

  vpc_config {
    subnet_ids         = lookup(var.subnet_ids_for_lambda, var.stage)
    security_group_ids = lookup(var.sg_for_lambda, var.stage)
  }
  environment {
    variables = {
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL = data.aws_ssm_parameter.api_base_url.value
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_API_KEY = data.aws_ssm_parameter.api_key.value
      CT_INBOUND_FOLDER_ID = data.aws_ssm_parameter.ct_inbound_folder_id.value
      CT_OUTBOUND_FOLDER_ID = data.aws_ssm_parameter.ct_outbound_folder_id.value
      EXCLUDED_CTAS_IDS =  data.aws_ssm_parameter.excluded_ctas_ids.value
    }
  }
   depends_on = [
    aws_s3_bucket_object.handler,
  ]
}

resource "aws_lambda_function" "here-to-help-lambda-SPL" {
  role             = aws_iam_role.here_to_help_role.arn
  handler          = var.spl_handler
  runtime          = var.runtime
  function_name    = var.SPL_function_name
  s3_bucket        = aws_s3_bucket.s3_deployment_artefacts.bucket
  s3_key           = aws_s3_bucket_object.handler.key
  source_code_hash = data.archive_file.lib_zip_file.output_base64sha256
  memory_size = 10240
  timeout = 900

  vpc_config {
    subnet_ids         = lookup(var.subnet_ids_for_lambda, var.stage)
    security_group_ids = lookup(var.sg_for_lambda, var.stage)
  }
  environment {
    variables = {
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL = data.aws_ssm_parameter.api_base_url.value
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_API_KEY = data.aws_ssm_parameter.api_key.value
      SPL_INBOUND_FOLDER_ID = data.aws_ssm_parameter.spl_inbound_folder_id.value
      SPL_OUTBOUND_FOLDER_ID = data.aws_ssm_parameter.spl_outbound_folder_id.value
    }
  }
   depends_on = [
    aws_s3_bucket_object.handler
  ]
}

resource "aws_lambda_function" "here-to-help-lambda-NSSS" {
  role             = aws_iam_role.here_to_help_role.arn
  handler          = var.nsss_handler
  runtime          = var.runtime
  function_name    = var.NSSS_function_name
  s3_bucket        = aws_s3_bucket.s3_deployment_artefacts.bucket
  s3_key           = aws_s3_bucket_object.handler.key
  source_code_hash = data.archive_file.lib_zip_file.output_base64sha256
  memory_size = 10240
  timeout = 900

  vpc_config {
    subnet_ids         = lookup(var.subnet_ids_for_lambda, var.stage)
    security_group_ids = lookup(var.sg_for_lambda, var.stage)
  }
  environment {
    variables = {
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL = data.aws_ssm_parameter.api_base_url.value
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_API_KEY = data.aws_ssm_parameter.api_key.value
      CEV_INBOUND_FOLDER_ID = data.aws_ssm_parameter.cev_inbound_folder_id.value
      CEV_OUTBOUND_FOLDER_ID = data.aws_ssm_parameter.cev_outbound_folder_id.value
    }
  }
   depends_on = [
    aws_s3_bucket_object.handler
  ]
}

resource "aws_lambda_function" "here-to-help-lambda-self-isolation" {
  role             = aws_iam_role.here_to_help_role.arn
  handler          = var.self_isolation_handler
  runtime          = var.runtime
  function_name    = var.self_isolation_function_name
  s3_bucket        = aws_s3_bucket.s3_deployment_artefacts.bucket
  s3_key           = aws_s3_bucket_object.handler.key
  source_code_hash = data.archive_file.lib_zip_file.output_base64sha256
  memory_size = 10240
  timeout = 900

  vpc_config {
    subnet_ids         = lookup(var.subnet_ids_for_lambda, var.stage)
    security_group_ids = lookup(var.sg_for_lambda, var.stage)
  }
  environment {
    variables = {
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL = data.aws_ssm_parameter.api_base_url.value
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_API_KEY = data.aws_ssm_parameter.api_key.value
      SELF_ISOLATION_INBOUND_FOLDER_ID = data.aws_ssm_parameter.self_isolation_inbound_folder_id.value
      SELF_ISOLATION_OUTBOUND_FOLDER_ID = data.aws_ssm_parameter.self_isolation_outbound_folder_id.value
      ENV = var.stage
    }
  }
   depends_on = [
    aws_s3_bucket_object.handler
  ]
}

resource "aws_lambda_function" "here-to-help-lambda-generic-ingestion" {
  role             = aws_iam_role.here_to_help_role.arn
  handler          = var.generic_ingestion_handler
  runtime          = var.runtime
  function_name    = var.generic_ingestion_function_name
  s3_bucket        = aws_s3_bucket.s3_deployment_artefacts.bucket
  s3_key           = aws_s3_bucket_object.handler.key
  source_code_hash = data.archive_file.lib_zip_file.output_base64sha256
  memory_size = 10240
  timeout = 900

  vpc_config {
    subnet_ids         = lookup(var.subnet_ids_for_lambda, var.stage)
    security_group_ids = lookup(var.sg_for_lambda, var.stage)
  }
  environment {
    variables = {
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL = data.aws_ssm_parameter.api_base_url.value
      CV_19_RES_SUPPORT_V3_HELP_REQUESTS_API_KEY = data.aws_ssm_parameter.api_key.value
      GENERIC_INGESTION_INBOUND_FOLDER_ID = data.aws_ssm_parameter.generic_ingestion_inbound_folder_id.value
      GENERIC_INGESTION_OUTBOUND_FOLDER_ID = data.aws_ssm_parameter.generic_ingestion_outbound_folder_id.value
      ENV = var.stage
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
  schedule_expression = "rate(16 minutes)"
  is_enabled = true
}

resource "aws_cloudwatch_event_rule" "here-to-help-scheduled-event-SPL" {
  name                = "here-to-help-scheduled-event"
  description         = "Fires every one minutes"
  schedule_expression = "rate(16 minutes)"
  is_enabled = true
}

resource "aws_cloudwatch_event_rule" "here-to-help-scheduled-event-NSSS" {
  name                = "here-to-help-scheduled-event"
  description         = "Fires every one minutes"
  schedule_expression = "rate(16 minutes)"
  is_enabled = true
}

resource "aws_cloudwatch_event_rule" "here-to-help-scheduled-event-self-isolation" {
  name                = "here-to-help-scheduled-event"
  description         = "Fires every one minutes"
  schedule_expression = "rate(16 minutes)"
  is_enabled = true
}

resource "aws_cloudwatch_event_rule" "here-to-help-scheduled-event-generic-ingestion" {
  name                = "here-to-help-scheduled-event"
  description         = "Fires every one minutes"
  schedule_expression = "rate(16 minutes)"
  is_enabled = true
}


resource "aws_cloudwatch_event_target" "check_google_sheet_spl" {
  rule      = aws_cloudwatch_event_rule.here-to-help-scheduled-event-SPL.name
  target_id = "here-to-help-lambda-spl"
  arn       = aws_lambda_function.here-to-help-lambda-SPL.arn
}

resource "aws_cloudwatch_event_target" "check_google_sheet_nsss" {
  rule      = aws_cloudwatch_event_rule.here-to-help-scheduled-event-NSSS.name
  target_id = "here-to-help-lambda-nsss"
  arn       = aws_lambda_function.here-to-help-lambda-NSSS.arn
}

resource "aws_cloudwatch_event_target" "check_google_sheet_self_isolation" {
  rule      = aws_cloudwatch_event_rule.here-to-help-scheduled-event-self-isolation.name
  target_id = "here-to-help-lambda-self-isolation"
  arn       = aws_lambda_function.here-to-help-lambda-self-isolation.arn
}

resource "aws_cloudwatch_event_target" "check_google_sheet_generic_ingestion" {
  rule      = aws_cloudwatch_event_rule.here-to-help-scheduled-event-generic-ingestion.name
  target_id = "here-to-help-lambda-generic-ingestion"
  arn       = aws_lambda_function.here-to-help-lambda-generic-ingestion.arn
}

resource "aws_lambda_permission" "allow_lambda_logging_and_call_check_google_sheet" {
  statement_id_prefix  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.here-to-help-lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.here-to-help-scheduled-event.arn
}

resource "aws_lambda_permission" "allow_lambda_logging_and_call_check_google_sheet-SPL" {
  statement_id_prefix  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.here-to-help-lambda-SPL.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.here-to-help-scheduled-event-SPL.arn
}

resource "aws_lambda_permission" "allow_lambda_logging_and_call_check_google_sheet-NSSS" {
  statement_id_prefix  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.here-to-help-lambda-NSSS.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.here-to-help-scheduled-event-NSSS.arn
}

resource "aws_lambda_permission" "allow_lambda_logging_and_call_check_google_sheet-self-isolation" {
  statement_id_prefix  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.here-to-help-lambda-self-isolation.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.here-to-help-scheduled-event-self-isolation.arn
}

resource "aws_lambda_permission" "allow_lambda_logging_and_call_check_google_sheet-generic-ingestion" {
  statement_id_prefix  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.here-to-help-lambda-generic-ingestion.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.here-to-help-scheduled-event-generic-ingestion.arn
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
        "ec2:AttachNetworkInterface",
        "ec2:DescribeRouteTables",
        "ec2:CreateRoute",
        "ec2:DeleteRoute",
        "ec2:ReplaceRoute",
        "ssm:Describe*",
        "ssm:Get*",
        "ssm:List*"
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

resource "aws_sns_topic" "here-to-help-data-ingestion" {
  name = "here-to-help-data-ingestion"
}

resource "aws_sns_topic_subscription" "here-to-help-data-ingestion-email-subscription" { 
  count = length(local.emails)
  topic_arn = aws_sns_topic.here-to-help-data-ingestion.arn
  protocol  = "email"
  endpoint  = element(local.emails, count.index)
}

resource "aws_cloudwatch_log_metric_filter" "here-to-help-lambda" {
  count = length(var.data_ingestion_function_names)
  name           = "${element(var.data_ingestion_function_names, count.index)}-error-filter"
  pattern        = "ERROR"
  log_group_name = "/aws/lambda/${element(var.data_ingestion_function_names, count.index)}"

  metric_transformation {
    name          = "CloudWatchLogError"
    namespace     = "ErrorCount"
    value         = 1
  }
  depends_on = [
    aws_lambda_function.here-to-help-lambda,
    aws_lambda_function.here-to-help-lambda-SPL,
    aws_lambda_function.here-to-help-lambda-NSSS,
    aws_lambda_function.here-to-help-lambda-self-isolation,
    aws_lambda_function.here-to-help-lambda-generic-ingestion
  ]
}

resource "aws_cloudwatch_metric_alarm" "here-to-help-data-ingestion" {
  alarm_name                = "here-to-help-data-ingestion"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "5"
  datapoints_to_alarm       = "4"
  metric_name               = "CloudWatchLogError"
  namespace                 = "ErrorCount"
  period                    = "300"
  statistic                 = "Sum"
  threshold                 = "2"
  treat_missing_data        = "missing"
  alarm_description         = "This metric monitors errors on the here-to-help-ingestion lambda logs"
  alarm_actions             = [ aws_sns_topic.here-to-help-data-ingestion.arn ]
  depends_on = [aws_sns_topic.here-to-help-data-ingestion]
}

resource "aws_cloudwatch_log_metric_filter" "here-to-help-lambda-warnings" {
  count = length(var.data_ingestion_function_names)
  name           = "${element(var.data_ingestion_function_names, count.index)}-warning-filter"
  pattern        = "INGEST_WARNING"
  log_group_name = "/aws/lambda/${element(var.data_ingestion_function_names, count.index)}"

  metric_transformation {
    name          = "CloudWatchLogWarning"
    namespace     = "WarningCount"
    value         = 1
  }
  depends_on = [
    aws_lambda_function.here-to-help-lambda,
    aws_lambda_function.here-to-help-lambda-SPL,
    aws_lambda_function.here-to-help-lambda-NSSS,
    aws_lambda_function.here-to-help-lambda-self-isolation,
    aws_lambda_function.here-to-help-lambda-generic-ingestion
  ]
}

resource "aws_cloudwatch_metric_alarm" "here-to-help-data-ingestion-warnings" {
  alarm_name                = "here-to-help-data-ingestion-warnings"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "1"
  datapoints_to_alarm       = "1"
  metric_name               = "CloudWatchLogWarning"
  namespace                 = "WarningCount"
  period                    = "43200"
  statistic                 = "Sum"
  threshold                 = "1"
  treat_missing_data        = "missing"
  alarm_description         = "This metric monitors warnings on the here-to-help-ingestion lambda logs"
  alarm_actions             = [ aws_sns_topic.here-to-help-data-ingestion.arn ]
  depends_on = [aws_sns_topic.here-to-help-data-ingestion]
}