import datetime as dt
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build

# Hopefully Kat has sorted the authentication part
# You can make keys by going to https://console.cloud.google.com/iam-admin/
# However that means you need access to the service account, which might
# only be for me [Huu Do]

# key_file_location = 'Here2HelpKey.json'


class GoogleDriveGateway:

    def __init__(self, key_file_location):
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location,
            scopes=scopes
        )

        self.drive_service = build('drive', 'v3', credentials=credentials)

    def search_folder(self, folder_id: str, target_date: str, file_type: str):
        """returns true/false if there are new files that match the date given."""

        # Drive_service(call google api).Files(the files part of the api).List(list function)
        # includeItemsFromAllDrives=True,supportsAllDrives=True
        #   <- Required for items you have not opened the item
        # fields="files(id, name, exportLinks, createdTime)"
        #   <--- What fields do we want?
        # q = "'Folder ID' in parents",
        #   <--- this filters for only files in the Folder ID. Put this in List()

        # File Found Count. Maybe we want to do something with the amount of
        # files we find
        foundcount = 0

        # Gives us a nice link to click and open the drive...in probably the wrong browser.
        # Copy Paste Recommended
        print(
            "[CheckFile: %s] Looking for files in \
            folder: https://drive.google.com/drive/folders/%s" %
            (dt.datetime.now(), folder_id)
        )

        # This makes the file list with the fields we want. In the folder ID passed to it
        # Field parameters here -
        # https://developers.google.com/drive/api/v3/reference/files

        # this [q = "stuff"] is quite confusing. Its basically only returning files which satisfy Q,
        # but its done in a non logical way
        # Documentation for q = Filter - https://developers.google.com/drive/api/v3/search-files
        # So trashed = false exists because its able to read trashed files which is
        # a disaster at best mimeType only looks for certain file types. So ive set it to sheets.
        # sheets is "spreadsheet"
        filelist = self.drive_service.files().list(
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            q="'%s' in parents and trashed=False and mimeType = 'application/vnd.google-apps.%s'" %
            (folder_id,
             file_type),
            fields="files(id, name, createdTime)").execute()

        items = filelist.get('files', [])

        for j in items:
            # anotherTestTime = j.get('createdTime')
            # print(anotherTestTime)
            testime = j.get('createdTime')[0:10]
            if testime == target_date:
                file_name = j.get('name')
                print(
                    "[CheckFile: %s] Found a file: %s" %
                    (dt.datetime.now(), file_name))
                foundcount += 1

        if foundcount > 0:
            print(
                "[CheckFile: %s] Files Found. Will Return True" %
                dt.datetime.now())
            return True

        print(
            "[CheckFile: %s] No File Found. Will return false" %
            dt.datetime.now())
        return False

    # returns file id to be used to read file
    def get_file(self, folder_id: str, target_date: str, file_type: str):
        file_id = ""
        # Note: I have no idea what it does if two files are made in there at the same time.
        # I expect horrific stuff
        # made it so if 0 or 2+ files are found. dont return file ID

        foundcount = 0
        print(
            "[get_file: %s] Looking for files in folder: \
            https://drive.google.com/drive/folders/%s" %
            (dt.datetime.now(), folder_id))
        filelist = self.drive_service.files().list(
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            q="'%s' in parents and trashed=False and mimeType = 'application/vnd.google-apps.%s'" %
            (folder_id,
             file_type),
            fields="files(id, name, createdTime)").execute()
        items = filelist.get('files', [])

        for j in items:
            # anotherTestTime = j.get('createdTime')
            # print(anotherTestTime)
            testime = j.get('createdTime')[0:10]
            if testime == target_date:
                file_id = j.get('id')
                print(
                    "[get_file: %s] Found ID: %s" %
                    (dt.datetime.now(), file_id))
                foundcount += 1

        if foundcount == 1:
            print(
                "[get_file: %s] Only ONE file found. Will return ID" %
                dt.datetime.now())
            return file_id

        print(
            "[get_file: %s] Error: 0 or more than 1 file found." %
            dt.datetime.now())
        return ""

    def create_spreadsheet(self, destination_folder, file_name):
        folder_id = destination_folder
        file_metadata = {
            'name': file_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': [folder_id]
        }

        spreadsheet = self.drive_service.files().create(
            supportsAllDrives=True, body=file_metadata, fields='id').execute()

        file_id = spreadsheet.get('id')
        print(file_id)
        return file_id
