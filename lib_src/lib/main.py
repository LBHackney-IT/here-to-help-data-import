from .gateways.here_to_help_api import HereToHelpGateway
from .gateways.gspread_drive_gateway import GSpreadGateway
from .gateways.google_drive_gateway import GoogleDriveGateway
from .usecase.create_help_requests import CreateHelpRequest
from .usecase.find_and_process_new_sheet import FindAndProcessNewSheet
from .lambda_handler import LambdaHandler
from dotenv import load_dotenv
import json

load_dotenv()


def lambda_handler(event, context):
    here_to_help_gateway = HereToHelpGateway()
    create_help_request = CreateHelpRequest(gateway=here_to_help_gateway)
    handler = LambdaHandler(create_help_request)

    google_drive_gateway = GoogleDriveGateway("key_file_location")
    gspread_drive_gateway = GSpreadGateway("key_file_location", google_drive_gateway)

    find_and_process_new_sheet = FindAndProcessNewSheet(google_drive_gateway, gspread_drive_gateway)

    folders = json.loads(event)

    find_and_process_new_sheet.execute(folders["inbound_folder_id"], folders["outbound_folder_id"])

    print("event: ", event, "context:", context)
    response = handler.execute(event, context)
    return response

