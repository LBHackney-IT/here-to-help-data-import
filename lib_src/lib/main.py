from dotenv import load_dotenv
from .gateways.here_to_help_api import HereToHelpGateway
from .gateways.pygsheets_gateway import PygsheetsGateway
from .gateways.google_drive_gateway import GoogleDriveGateway
from .usecase.create_help_requests import CreateHelpRequest
from .usecase.find_and_process_new_sheet import FindAndProcessNewSheet
# from .lambda_handler import LambdaHandler
from .usecase.add_hackney_cases_to_app import AddHackneyCasesToApp
from os import path
import requests

load_dotenv()

def lambda_handler(event, context):

    print('- -start up - -')

    response = requests.get("http://dummy.restapiexample.com/api/v1/employees")

    print('api test: ', response.status_code)

    here_to_help_gateway = HereToHelpGateway()
    create_help_request = CreateHelpRequest(gateway=here_to_help_gateway)
    # handler = LambdaHandler(create_help_request)
    #
    # response = handler.execute(event, context)

    key_file_location = path.relpath('lib/key_file.json')

    google_drive_gateway = GoogleDriveGateway(key_file_location)

    pygsheets_gateway = PygsheetsGateway(
        key_file_location,
        google_drive_gateway
    )

    add_hackney_cases_to_app = AddHackneyCasesToApp(create_help_request)

    find_and_process_new_sheet = FindAndProcessNewSheet(
        google_drive_gateway, pygsheets_gateway, add_hackney_cases_to_app)

    response = find_and_process_new_sheet.execute(
        event.get("inbound_folder_id"),
        event.get("outbound_folder_id"))

    return response
