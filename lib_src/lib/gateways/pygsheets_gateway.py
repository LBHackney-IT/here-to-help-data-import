from datetime import datetime
import numpy as np
import pygsheets

# Hopefully Kat has sorted the authentication part
# You can make keys by going to https://console.cloud.google.com/iam-admin/
# However that means you need access to the service account, which might
# only be for me [Huu Do]

# key_file_location = 'Here2HelpKey.json'

class PygsheetsGateway:

    DRIVE = "/content/drive/Shared drives/Here To Help Project Team/Data/"
    INPUT = 'T&T daily extracts'
    OUTPUT = 'T&T daily outputs'
    SHEET_NAME = 'Sheet1'
    FIND_TERM = 'Category'
    # have also included NHS Number, 'Date Updated', 'Date Time Extracted' as
    # would be useful for data warehouse etc
    COLS = [
        'Account ID',
        'NHS Number',
        'Forename',
        'Surname',
        'Gender',
        'Date of Birth',
        'House Number',
        'Postcode',
        'Email',
        'Phone',
        'Phone2',
        'First Symptomatic At',
        'Date Tested',
        'Comments',
        'Date Updated',
        'Date Time Extracted']

    def __init__(self, key_file_location):

        self.gsheet_service = pygsheets.authorize(service_file=key_file_location)

    def get_cases_from_gsheet(self, sheet_key):
        # print(
        #     "[get_cases_from_gsheet] Trying to open by key using %s" %
        #     sheet_key)
        spreadsheet = self.gsheet_service.open_by_key(sheet_key)
        # print(spreadsheet)
        sheet = spreadsheet.worksheet('index', 0)  # CHANGEINCODE - finds first sheet instead
        data_frame = sheet.get_as_df(start='A3', parse_dates=True)  # CHANGEINCODE - different sheet loading style
        data_frame = data_frame.convert_dtypes()
        data_frame = self.clean_data(data_frame=data_frame)
        # print("[get_cases_from_gsheet] Displaying Dataframe")
        # print(data_frame)
        return data_frame  # returns dataframe

    def clean_data(self, data_frame):  # takes whole sheet and lints data
        for i in self.COLS:
            data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'\s+', '')
            data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'nan', np.nan)

        # some account ids are just numbers, we need them to be string
        data_frame['Account ID'] = data_frame['Account ID'].astype(str)
        return data_frame

    def populate_spreadsheet(self, data_frame, spreadsheet_key):
        spreadsheet = self.gsheet_service.open_by_key(spreadsheet_key)
        # loop through each created dataframe and populate spreadsheet
        for sheet in data_frame:
            data_frame = sheet[0]
            title = sheet[1]
            worksheet = spreadsheet.add_worksheet(title=title)
            worksheet.set_dataframe(df=data_frame, start='A1', fit=True)

        sheet1 = spreadsheet.worksheet('title', 'Sheet1')  # CHANGEINCODE - different worksheet pull

        spreadsheet.del_worksheet(sheet1)  # CHANGEINCODE - different worksheet delete

    def next_available_row(self, worksheet):
        # print("[next_available_row]")
        str_list = list(filter(None, worksheet.col_values(1)))
        return str(len(str_list) + 1)
