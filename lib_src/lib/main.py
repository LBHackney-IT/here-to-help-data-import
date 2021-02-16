from dotenv import load_dotenv
from .gateways.here_to_help_api import HereToHelpGateway
from .gateways.pygsheets_gateway import PygsheetsGateway
from .gateways.google_drive_gateway import GoogleDriveGateway
from .usecase.create_help_requests import CreateHelpRequest
from .usecase.process_contact_tracing_calls import ProcessContactTracingCalls
# from .lambda_handler import LambdaHandler
from .usecase.add_contact_tracing_requests import AddContactTracingRequests
from os import getenv
from os import path

load_dotenv()

def lambda_handler(event, context):

    print('- -start up - -')

    here_to_help_gateway = HereToHelpGateway()

    create_help_request = CreateHelpRequest(gateway=here_to_help_gateway)

    key_file_location = path.relpath('lib/key_file.json')

    google_drive_gateway = GoogleDriveGateway(key_file_location)

    pygsheets_gateway = PygsheetsGateway(
        key_file_location
    )

    add_contact_tracing_requests = AddContactTracingRequests(create_help_request)

    find_and_process_contact_tracing = ProcessContactTracingCalls(
        google_drive_gateway, pygsheets_gateway, add_contact_tracing_requests)

    ct_inbound_folder_id = getenv("CT_INBOUND_FOLDER_ID")
    ct_outbound_folder_id = getenv("CT_OUTBOUND_FOLDER_ID")

    response = find_and_process_contact_tracing.execute(
        ct_inbound_folder_id,
        ct_outbound_folder_id
    )

    return response
