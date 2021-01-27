from datetime import datetime
import pygsheets

class PygsheetsGateway:
    def __init__(self, key_file_location):

        self.gsheet_service = pygsheets.authorize(service_file=key_file_location)

    def get_data_frame_from_sheet(self, sheet_key, start_cell):
        spreadsheet = self.gsheet_service.open_by_key(sheet_key)
        sheet = spreadsheet.worksheet('index', 0)  # CHANGEINCODE - finds first sheet instead
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
