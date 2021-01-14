from datetime import datetime
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import numpy as np
import gspread_dataframe as gspread_dataframe
from gspread_formatting import *


# Hopefully Kat has sorted the authentication part
# You can make keys by going to https://console.cloud.google.com/iam-admin/
# However that means you need access to the service account, which might
# only be for me [Huu Do]

# key_file_location = 'Here2HelpKey.json'


class GSpreadGateway:

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

    def __init__(self, key_file_location, google_drive_gateway):

        self.google_drive_gateway = google_drive_gateway
        scopes = ['https://spreadsheets.google.com/feeds']

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes)
        self.gspread_service = gspread.authorize(
            creds)  # makes the gspread service

    def get_cases_from_gsheet(self, sheet_key):
        print(
            "[get_cases_from_gsheet] Trying to open by key using %s" %
            sheet_key)
        spreadsheet = self.gspread_service.open_by_key(sheet_key)
        print(spreadsheet)
        sheet = spreadsheet.worksheet(self.SHEET_NAME)
        # find first cell in T&T dowbnload - this should be 'Category', and use
        # returned row value to get starting point of data
        first_cell = sheet.find(self.FIND_TERM)
        df = gspread_dataframe.get_as_dataframe(
            sheet, skiprows=2, parse_dates=True)
        df = df.convert_dtypes()
        df = self.clean_data(df=df)
        print("[get_cases_from_gsheet] Displaying Dataframe")
        # print(df)
        return df  # returns dataframe

    def clean_data(self, df):  # takes whole sheet and lints data
        for i in self.COLS:
            df[i] = df[i].astype(str).str.strip().replace(r'\s+', '')
            df[i] = df[i].astype(str).str.strip().replace(r'nan', np.nan)

        # some account ids are just numbers, we need them to be string
        df['Account ID'] = df['Account ID'].astype(str)
        return df

    def create_output_spreadsheet(self, data_frame, outbound_folder_id):
        print("[create_output_spreadsheet]")
        # get today's date for new filename
        today = datetime.today().strftime('%d/%m/%Y')
        # create new filename
        new_spreadsheet_name = f'Hackney_CT_FOR_UPLOAD_{today}'
        # create a new spreadsheet TODO this only writes to personal drive so
        # need way to write to shared drive - service account better for this?

        sh = self.gspread_service.open_by_key(
            self.google_drive_gateway.create_spreadsheet(
                outbound_folder_id, new_spreadsheet_name))
        print(sh)

        # loop through each created dataframe and populate spreadsheet
        for i in data_frame:
            print(i[1])
            self.populate_output_sheets(spreadsheet=sh, df=i[0], title=i[1])
        sheet1 = sh.get_worksheet(0)
        sh.del_worksheet(sheet1)

        print(f'spreadsheet {new_spreadsheet_name} created.')

    def create_city_spreadsheet(self, data_frame, outbound_folder_id):
        print("[create_city_spreadsheet]")
        # get today's date for new filename
        today = datetime.today().strftime('%d/%m/%Y')
        # create new filename
        new_spreadsheet_name = f'city_CT_FOR_UPLOAD_{today}'
        # create a new spreadsheet TODO this only writes to personal drive so
        # need way to write to shared drive - service account better for this?
        sh = self.gspread_service.open_by_key(
            self.google_drive_gateway.create_spreadsheet(
                outbound_folder_id, new_spreadsheet_name))
        # loop through each created dataframe and populate spreadsheet
        for i in data_frame:
            print(i[1])
            self.populate_output_sheets(spreadsheet=sh, df=i[0], title=i[1])

        sheet1 = sh.get_worksheet(0)
        sh.del_worksheet(sheet1)
        print(f'spreadsheet {new_spreadsheet_name} created.')

        # should we update this to write to csv or xlsx?

    def populate_output_sheets(self, spreadsheet, df, title):
        print("[populate_output_sheets]")
        # add a tab for each file and write each dataframe
        worksheet = spreadsheet.add_worksheet(
            title=title, rows=df.shape[0] + 10, cols=len(self.COLS))
        next_row = self.next_available_row(worksheet)
        gspread_dataframe.set_with_dataframe(
            worksheet, df, include_column_header=True, row=int(next_row), col=1)
        # set_row_height(worksheet, f'1:{df.shape[0] + 10}', 21)
        return

    def next_available_row(self, worksheet):
        print("[next_available_row]")
        str_list = list(filter(None, worksheet.col_values(1)))
        return str(len(str_list) + 1)
