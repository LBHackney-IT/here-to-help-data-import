from .gateways.here_to_help_api import HereToHelpGateway
from .usecase.create_help_requests import CreateHelpRequest
from .lambda_handler import LambdaHandler
from dotenv import load_dotenv

load_dotenv()


def lambda_handler(event, context):
    here_to_help_gateway = HereToHelpGateway()
    create_help_request = CreateHelpRequest(gateway=here_to_help_gateway)
    handler = LambdaHandler(create_help_request)
    print("event: ", event, "context:", context)
    response = handler.execute(event, context)
    return response
