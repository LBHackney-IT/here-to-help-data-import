from .usecase.create_help_request import CreateHelpRequest
from .lambda_handler import LambdaHandler


def lambda_handler(event, context):
    create_help_request = CreateHelpRequest()
    handler = LambdaHandler(create_help_request)
    return handler.execute(event, context)

