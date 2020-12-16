from .gateways.here_to_help_api import HereToHelpGateway
from .usecase.create_help_request import CreateHelpRequest
from .lambda_handler import LambdaHandler
import glob
import os
import datetime as dt
# from gspread_formatting import *

# Connect and Authenticate Google Drive
# from google.colab import drive
import importlib

from dotenv import load_dotenv
load_dotenv()


def checkFileToday(folderPath: str, todaysDate: str, fileType: str):
    print("[checkFileToday] Checking files in: " + folderPath)
    print("[checkFileToday] Using Date: " + todaysDate)
    folderPath = folderPath + "*." + fileType
    foundcount = 0

    extractFiles = glob.glob(folderPath)
    files = []
    for i in extractFiles:
        files.append(i)

    for j in files:
        testime = dt.datetime.fromtimestamp(os.path.getctime(j)).strftime('%Y-%m-%d')
        if testime == todaysDate:
            filename = os.path.split(j)
            print("[checkFileToday] Found a file: " + filename[1])
            foundcount += 1

    if foundcount > 0:
        print("[checkFileToday] Files Found. Will Return True")
        print("")
        return True
    # elif foundcount >1:
    #   print("[checkFileToday] More than 1 File Found. Will return false")
    #   print("")
    #   return False
    elif foundcount == 0:
        print("[checkFileToday] No File Found. Will return false")
        print("")
        return False

def lambda_handler(event, context):
    # add authentication here
    # importlib.reload(drive)
    #
    # drive.mount('/content/drive')
    # Path Define for folders

    tat_daily_outputs_folder = "/content/drive/Shareddrives/Here To Help Project Team/Data/T&T daily outputs/"
    tat_daily_extracts_folder = "/content/drive/Shareddrives/Here To Help Project Team/Data/T&T daily extracts/"
    hth_daily_extracts_folder = '/content/drive/Shareddrives/Here To Help Project Team/Data/Here to Help daily extracts/'

    # Path Define for Files

    # Get Today in usable form

    today = dt.datetime.now().date().strftime('%Y-%m-%d')
    print("[define_paths] " + "Paths Defined for Import and Export")
    print(" ")

    if checkFileToday(tat_daily_extracts_folder, today, "gsheet") == True & checkFileToday(tat_daily_outputs_folder,today, "gsheet") == False:
        print("success")
    else:
        print("Fail")


    here_to_help_gateway = HereToHelpGateway()
    create_help_request = CreateHelpRequest(gateway=here_to_help_gateway)

    handler = LambdaHandler(create_help_request)
    print("event: ", event, "context:", context)
    return handler.execute(event, context)
