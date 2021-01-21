from dotenv import load_dotenv
from .gateways.here_to_help_api import HereToHelpGateway
from .gateways.gspread_drive_gateway import GSpreadGateway
from .gateways.google_drive_gateway import GoogleDriveGateway
from .usecase.create_help_requests import CreateHelpRequest
from .usecase.find_and_process_new_sheet import FindAndProcessNewSheet
from .lambda_handler import LambdaHandler
from os import path
from os import listdir
from os import getcwd
import json

load_dotenv()

def lambda_handler(event, context):
    print("event: ", event, "context:", context)

    print('-------------------------------------')

    key_file_location = path.relpath('lib/key_file.json')

    print(key_file_location)

    here_to_help_gateway = HereToHelpGateway()
    create_help_request = CreateHelpRequest(gateway=here_to_help_gateway)
    handler = LambdaHandler(create_help_request)

    print('google_drive_gateway init start')

    google_drive_gateway = GoogleDriveGateway(key_file_location)

    print('google_drive_gateway init done')

    print('gspread_drive_gateway init start')

    gspread_drive_gateway = GSpreadGateway(
        key_file_location,
        google_drive_gateway
    )

    print('gspread_drive_gateway init done')

    print('find_and_process_new_sheet init start')
    find_and_process_new_sheet = FindAndProcessNewSheet(
        google_drive_gateway, gspread_drive_gateway)

    print('find_and_process_new_sheet init done')

    folders = json.loads(event)

    print('folders: ', folders)

    print('find_and_process_new_sheet execute start')

    find_and_process_new_sheet.execute(
        folders["inbound_folder_id"],
        folders["outbound_folder_id"])

    print('find_and_process_new_sheet execute done')

    response = handler.execute(event, context)
    return response
