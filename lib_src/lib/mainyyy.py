import json
from dotenv import load_dotenv
from gateways.here_to_help_api import HereToHelpGateway
from gateways.gspread_drive_gateway import GSpreadGateway
from gateways.google_drive_gateway import GoogleDriveGateway
from usecase.create_help_requests import CreateHelpRequest
from usecase.find_and_process_new_sheet import FindAndProcessNewSheet
from lambda_handler import LambdaHandler

load_dotenv()
import sys


def lambda_handler(event, context):
    # here_to_help_gateway = HereToHelpGateway()
    # create_help_request = CreateHelpRequest(gateway=here_to_help_gateway)
    # handler = LambdaHandler(create_help_request)
    print(sys.version)

    print("------- Getting key_file_location")
    #
    # key_file_location = 'key_file.json'
    # google_drive_gateway = GoogleDriveGateway(key_file_location)
    # gspread_drive_gateway = GSpreadGateway(
    #     key_file_location, google_drive_gateway)
    #
    # find_and_process_new_sheet = FindAndProcessNewSheet(
    #     google_drive_gateway, gspread_drive_gateway)
    #
    # # folders = json.loads(event)
    #
    # print("event: ", event, "context:", context)
    #
    # # inbound_folder_id = '1sh35k9J-a4AaOQFDGaePcHAeSpo45sC8' -- HUU
    # # outbound_folder_id = '1zEdMiqPE9wWEZ-xuOHA13YzA2a5aKW-3' -HUU
    #
    # inbound_folder_id =  "1q5PBMtbv6RZY_V9dsCI54EJSGQCaXOgQ"
    # outbound_folder_id = "1WistgfO5q4XbLLpV9g060kYs7JIw956g"
    #
    # find_and_process_new_sheet.execute(
    #     inbound_folder_id,
    #     outbound_folder_id
    # )

    # find_and_process_new_sheet.execute(
    #     folders["inbound_folder_id"],
    #     folders["outbound_folder_id"]
    # )
    print(sys.version)
    # print("event: ", event, "context:", context)
    # response = handler.execute(event, context)
    # return response

if __name__ == '__main__':
    lambda_handler('event', 'context');
