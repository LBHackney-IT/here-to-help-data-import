import json
from dotenv import load_dotenv
from .gateways.here_to_help_api import HereToHelpGateway
# from .gateways.gspread_drive_gateway import GSpreadGateway
from .gateways.google_drive_gateway import GoogleDriveGateway
from .usecase.create_help_requests import CreateHelpRequest
# from .usecase.find_and_process_new_sheet import FindAndProcessNewSheet
from .lambda_handler import LambdaHandler
import os

load_dotenv()

def lambda_handler(event, context):
    here_to_help_gateway = HereToHelpGateway()
    create_help_request = CreateHelpRequest(gateway=here_to_help_gateway)
    handler = LambdaHandler(create_help_request)

    print("------- Getting key_file_location")

    key_file_location = 'lib/key_file.json'
    print(os.getcwd())
    real_location = os.path.realpath(key_file_location)

    print('real_location', real_location)
    print('     ')

    print('os.listdir("lib/")', os.listdir("lib/"))
    print('     ')
    print('os.listdir("./")', os.listdir("./"))


    google_drive_gateway = GoogleDriveGateway(real_location)

    print(google_drive_gateway)
    # gspread_drive_gateway = GSpreadGateway(
    #     key_file_location, google_drive_gateway)
    #
    # find_and_process_new_sheet = FindAndProcessNewSheet(
    #     google_drive_gateway, gspread_drive_gateway)
    #
    # folders = json.loads(event)
    #
    # print("event: ", event, "context:", context)
    #
    # find_and_process_new_sheet.execute(
    #     folders["inbound_folder_id"],
    #     folders["outbound_folder_id"])

    response = handler.execute(event, context)
    return response
