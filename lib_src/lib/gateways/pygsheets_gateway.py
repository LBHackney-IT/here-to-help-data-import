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

    def __init__(self, key_file_location, google_drive_gateway):

        self.google_drive_gateway = google_drive_gateway

        print('    GSpreadGateway gsheet_service start')

        self.gsheet_service = pygsheets.authorize(service_file=key_file_location)

        print('    GSpreadGateway gsheet_service start')

    def get_cases_from_gsheet(self, sheet_key):
        print(
            "[get_cases_from_gsheet] Trying to open by key using %s" %
            sheet_key)
        spreadsheet = self.gsheet_service.open_by_key(sheet_key)
        print(spreadsheet)
        sheet = spreadsheet.worksheet('index', 0)  # CHANGEINCODE - finds first sheet instead
        data_frame = sheet.get_as_df(start='A3', parse_dates=True)  # CHANGEINCODE - different sheet loading style
        data_frame = data_frame.convert_dtypes()
        data_frame = self.clean_data(data_frame=data_frame)
        print("[get_cases_from_gsheet] Displaying Dataframe")
        # print(data_frame)
        return data_frame  # returns dataframe

    def clean_data(self, data_frame):  # takes whole sheet and lints data
        for i in self.COLS:
            data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'\s+', '')
            data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'nan', np.nan)

        # some account ids are just numbers, we need them to be string
        data_frame['Account ID'] = data_frame['Account ID'].astype(str)
        return data_frame

    def create_output_spreadsheet(self, data_frame, outbound_folder_id):
        print("[create_output_spreadsheet]")
        # get today's date for new filename
        today = datetime.today().strftime('%d/%m/%Y')
        # create new filename
        new_spreadsheet_name = f'Hackney_CT_FOR_UPLOAD_{today}'
        # create a new spreadsheet TODO this only writes to personal drive so
        # need way to write to shared drive - service account better for this?

        spreadsheet = self.gsheet_service.open_by_key(
            self.google_drive_gateway.create_spreadsheet(
                outbound_folder_id, new_spreadsheet_name))
        print(spreadsheet)

        # loop through each created dataframe and populate spreadsheet
        for i in data_frame:
            print(i[1])
            self.populate_output_sheets(spreadsheet=spreadsheet, data_frame=i[0], title=i[1])
        sheet1 = spreadsheet.worksheet('title', 'Sheet1')  # CHANGEINCODE - different worksheet pull
        spreadsheet.del_worksheet(sheet1)  # CHANGEINCODE - different worksheet delete

        print(f'spreadsheet {new_spreadsheet_name} created.')

    def create_city_spreadsheet(self, data_frame, outbound_folder_id):
        print("[create_city_spreadsheet]")
        # get today's date for new filename
        today = datetime.today().strftime('%d/%m/%Y')
        # create new filename
        new_spreadsheet_name = f'city_CT_FOR_UPLOAD_{today}'
        # create a new spreadsheet TODO this only writes to personal drive so
        # need way to write to shared drive - service account better for this?
        spreadsheet = self.gsheet_service.open_by_key(
            self.google_drive_gateway.create_spreadsheet(
                outbound_folder_id, new_spreadsheet_name))
        # loop through each created dataframe and populate spreadsheet
        for i in data_frame:
            print(i[1])
            self.populate_output_sheets(spreadsheet=spreadsheet, data_frame=i[0], title=i[1])

        sheet1 = spreadsheet.worksheet('title', 'Sheet1')  # CHANGEINCODE - different worksheet pull
        spreadsheet.del_worksheet(sheet1)  # CHANGEINCODE - different worksheet delete
        print(f'spreadsheet {new_spreadsheet_name} created.')

        # should we update this to write to csv or xlsx?

    def populate_output_sheets(self, spreadsheet, data_frame, title):
        print("[populate_output_sheets]")
        # add a tab for each file and write each dataframe

        worksheet = spreadsheet.add_worksheet(title=title)

        return worksheet.set_dataframe(df=data_frame, start='A1', fit=True)

    def next_available_row(self, worksheet):
        print("[next_available_row]")
        str_list = list(filter(None, worksheet.col_values(1)))
        return str(len(str_list) + 1)
