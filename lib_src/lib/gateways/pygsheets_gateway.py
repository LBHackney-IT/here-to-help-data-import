from datetime import datetime
import pygsheets
from ..helpers import is_within_collection

class PygsheetsGateway:
    def __init__(self, key_file_location):

        self.gsheet_service = pygsheets.authorize(service_file=key_file_location)

    def get_data_frame_from_sheet(self, sheet_key, start_cell):
        spreadsheet = self.gsheet_service.open_by_key(sheet_key)
        sheet = spreadsheet.worksheet('index', 0)  # CHANGEINCODE - finds first sheet instead
        
        # If the headers are not within the first 10 rows, then something is seriously off with the sheet.
        # It would't be a good idea to iterate over, say, 1'000 rows just to find out they're missing.
        rawVals = sheet.get_all_values()[:10]

        start_cell=''
        for index, row in enumerate(rawVals):
            if(is_within_collection('Account ID', row) and is_within_collection('Forename', row) and is_within_collection('Surname', row)):
                # Assuming that table starts at the 1st (A) column.
                start_cell=f'A{index+1}'
                print(start_cell , 'headers identified')
            else:
                # Maybe reduce range to reduce logs?
                print(index + 1, 'row - no headers')

        data_frame = sheet.get_as_df(start=start_cell, parse_dates=True)  # CHANGEINCODE - different sheet loading style
        data_frame = data_frame.convert_dtypes()

        return data_frame  # returns dataframe

    def populate_spreadsheet(self, sheet_array, spreadsheet_key):
        spreadsheet = self.gsheet_service.open_by_key(spreadsheet_key)
        # loop through each created dataframe and populate spreadsheet
        for sheet in sheet_array:
            title = sheet['sheet_title']
            data_frame = sheet['data_frame']
            worksheet = spreadsheet.add_worksheet(title=title)
            worksheet.set_dataframe(df=data_frame, start='A1', fit=True)

        sheet1 = spreadsheet.worksheet('title', 'Sheet1')  # CHANGEINCODE - different worksheet pull

        spreadsheet.del_worksheet(sheet1)  # CHANGEINCODE - different worksheet delete
