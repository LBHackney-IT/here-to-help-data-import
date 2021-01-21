from dotenv import load_dotenv
from .gateways.here_to_help_api import HereToHelpGateway
from .gateways.pygsheets_gateway import PygsheetsGateway
from .gateways.google_drive_gateway import GoogleDriveGateway
from .usecase.create_help_requests import CreateHelpRequest
from .usecase.find_and_process_new_sheet import FindAndProcessNewSheet
from .lambda_handler import LambdaHandler
from os import path
import json

load_dotenv()

def lambda_handler(event, context):

    here_to_help_gateway = HereToHelpGateway()
    create_help_request = CreateHelpRequest(gateway=here_to_help_gateway)
    handler = LambdaHandler(create_help_request)

    response = handler.execute(event, context)

    print("event: ", event, "context:", context)

    print('-------------------------------------')

    key_file_location = path.relpath('lib/key_file.json')

    print(key_file_location)

    print('google_drive_gateway init start')

    google_drive_gateway = GoogleDriveGateway(key_file_location)

    print('google_drive_gateway init done')

    print('pygsheets_gateway init start')

    pygsheets_gateway = PygsheetsGateway(
        key_file_location,
        google_drive_gateway
    )

    print('pygsheets_gateway init done')

    print('find_and_process_new_sheet init start')
    find_and_process_new_sheet = FindAndProcessNewSheet(
        google_drive_gateway, pygsheets_gateway)

    print('find_and_process_new_sheet init done')

    print('find_and_process_new_sheet execute start')

    find_and_process_new_sheet.execute(
        event.get("inbound_folder_id"),
        event.get("outbound_folder_id"))

    print('find_and_process_new_sheet execute done')

    return response
