from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt

# Hopefully Kat has sorted the authentication part
# You can make keys by going to https://console.cloud.google.com/iam-admin/
# However that means you need access to the service account, which might only be for me [Huu Do]

# key_file_location = 'Here2HelpKey.json'


class GoogleDriveGateway:

    def __init__(self, key_file_location):
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location,
            scopes=scopes
        )

        self.drive_service = build('drive', 'v3', credentials=credentials)

    def searchFolder(self, folderID:str, targetDate: str, fileType:str): # returns true/false if there are new files that match the date given

        # Drive_service(call google api).Files(the files part of the api).List(list function)
        # includeItemsFromAllDrives=True,supportsAllDrives=True <- Required for items you have not opened the item
        # fields="files(id, name, exportLinks, createdTime)" <--- What fields do we want?
        # q = "'Folder ID' in parents", <--- this filters for only files in the Folder ID. Put this in List()

        # File Found Count. Maybe we want to do something with the amount of files we find
        foundcount = 0

        # Gives us a nice link to click and open the drive...in probably the wrong browser. Copy Paste Recommended
        print("[CheckFile: %s] Looking for files in folder: https://drive.google.com/drive/folders/%s" %(dt.datetime.now(),folderID))

        # This makes the file list with the fields we want. In the folder ID passed to it
        # Field parameters here - https://developers.google.com/drive/api/v3/reference/files

        # this [q = "stuff"] is quite confusing. Its basically only returning files which satisfy Q, but its done in a non logical way
        # Documentation for q = Filter - https://developers.google.com/drive/api/v3/search-files
        # So trashed = false exists because its able to read trashed files which is a disaster at best
        # mimeType only looks for certain file types. So ive set it to sheets. sheets is "spreadsheet"
        filelist = self.drive_service.files().list(includeItemsFromAllDrives=True,supportsAllDrives=True,q="'%s' in parents and trashed=False and mimeType = 'application/vnd.google-apps.%s'" %(folderID ,fileType),fields="files(id, name, createdTime)").execute()

        items = filelist.get('files', [])

        for j in items:
            # anotherTestTime = j.get('createdTime')
            # print(anotherTestTime)
            testime = j.get('createdTime')[0:10]
            if testime == targetDate:
                filename = j.get('name')
                print("[CheckFile: %s] Found a file: %s" %(dt.datetime.now(), filename))
                foundcount += 1

        if foundcount > 0:
            print("[CheckFile: %s] Files Found. Will Return True" % dt.datetime.now())
            return True

        elif foundcount == 0:
            print("[CheckFile: %s] No File Found. Will return false" % dt.datetime.now())
            return False

    def getFile(self, folderID: str, targetDate: str, fileType: str): # returns file id to be used to read file
            fileID = ""
            # Note: I have no idea what it does if two files are made in there at the same time. I expect horrific stuff
            # made it so if 0 or 2+ files are found. dont return file ID

            foundcount = 0
            print("[getFile: %s] Looking for files in folder: https://drive.google.com/drive/folders/%s" % (dt.datetime.now(), folderID))
            filelist = self.drive_service.files().list(includeItemsFromAllDrives=True, supportsAllDrives=True,
                                                  q="'%s' in parents and trashed=False and mimeType = 'application/vnd.google-apps.%s'" % (
                                                  folderID, fileType), fields="files(id, name, createdTime)").execute()
            items = filelist.get('files', [])

            for j in items:
                # anotherTestTime = j.get('createdTime')
                # print(anotherTestTime)
                testime = j.get('createdTime')[0:10]
                if testime == targetDate:
                    filename = j.get('name')
                    fileID = j.get('id')
                    print("[getFile: %s] Found ID: %s" % (dt.datetime.now(), fileID))
                    foundcount += 1

            if foundcount ==1:
                print("[getFile: %s] Only ONE file found. Will return ID" % dt.datetime.now())
                return fileID

            else :
                print("[getFile: %s] Error: 0 or more than 1 file found." % dt.datetime.now())

    def create_spreadsheet(self, destinationFolder, fileName):
        folder_id = destinationFolder
        file_metadata = {
            'name': fileName,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': [folder_id]
        }

        spreadsheet = self.drive_service.files().create(supportsAllDrives=True, body=file_metadata,
                                                   fields='id').execute()

        fileID = spreadsheet.get('id')
        print(fileID)
        return fileID
