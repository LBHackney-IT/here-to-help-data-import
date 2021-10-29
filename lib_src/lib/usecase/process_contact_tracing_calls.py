import datetime as dt
import numpy as np
from ..helpers import manual_parse


class ProcessContactTracingCalls:
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

    def __init__(self, google_drive_gateway, pygsheet_gateway, add_contact_tracing_requests):
        self.google_drive_gateway = google_drive_gateway
        self.pygsheet_gateway = pygsheet_gateway
        self.add_contact_tracing_requests = add_contact_tracing_requests

    def execute(self, inbound_folder_id, outbound_folder_id, excluded_ctas_ids):
        inbound_files = self.google_drive_gateway.get_list_of_files(
            inbound_folder_id)

        if not inbound_files:
            print(
                "No File found for today in folder: https://drive.google.com/drive/folders/%s " %
                inbound_folder_id)
            print("Will Abort")
            return 'not found'

        outbound_files = self.google_drive_gateway.get_list_of_files(
            outbound_folder_id)

        if len(inbound_files) * 2 == len(outbound_files):
            print(
                "Output files found in output folder: https://drive.google.com/drive/folders/%s " %
                outbound_folder_id)
            print("Will Abort")
            return 'all done'

        for file in inbound_files:
            today = dt.datetime.now().date().strftime('%Y-%m-%d')

            processed_file_name = f'Hackney_CT_FOR_UPLOAD_{file.get("name")}_{today}'

            if not any(
                    f['name'] == processed_file_name for f in outbound_files):
                print(
                    f'processing {processed_file_name}')

                inbound_spread_sheet_id = file.get('id')

                data_frame = self.pygsheet_gateway.get_data_frame_from_sheet(
                    inbound_spread_sheet_id, 'A3')

                if len(data_frame) < 3000:
                    data_frame = self.clean_data(data_frame=data_frame, excluded_ctas_ids=excluded_ctas_ids)

                    city_cases = self.get_city_cases(data_frame=data_frame)

                    hackney_cases = self.get_hackney_cases(data_frame=data_frame)

                    address_list, email_list = self.get_address_email_lists(
                        data_frame=hackney_cases)

                    city_spreadsheet = [{
                        'sheet_title': 'city_cases',
                        'data_frame': city_cases
                    }]

                    hackney_spreadsheet = [{
                        'sheet_title': 'email_list',
                        'data_frame': email_list
                    }, {
                        'sheet_title': 'address_list',
                        'data_frame': address_list
                    }, {
                        'sheet_title': 'hackney_cases',
                        'data_frame': hackney_cases
                    }]

                    self.add_contact_tracing_requests.execute(hackney_cases)

                    today = dt.datetime.now().date().strftime('%Y-%m-%d')

                    hackney_output_spreadsheet_key = self.google_drive_gateway.create_spreadsheet(
                        outbound_folder_id, f'Hackney_CT_FOR_UPLOAD_{file.get("name")}_{today}')

                    self.pygsheet_gateway.populate_spreadsheet(
                        hackney_spreadsheet, spreadsheet_key=hackney_output_spreadsheet_key)

                    city_spreadsheet_key = self.google_drive_gateway.create_spreadsheet(
                        outbound_folder_id, f'city_CT_FOR_UPLOAD_{file.get("name")}_{today}')

                    self.pygsheet_gateway.populate_spreadsheet(
                        city_spreadsheet, spreadsheet_key=city_spreadsheet_key)
                else:
                    print("Error: Contact Tracing sheet exceeded 3000 rows and was skipped. File found in \
                    inbound folder: https://drive.google.com/drive/folders/%s " %
                          (inbound_folder_id))

                break

    @classmethod
    def get_city_cases(cls, data_frame):
        # print("[get_city_cases] Creating COL Case Dataframe")
        city_data_frame = data_frame[data_frame['UTLA'] == 'City of London']
        # print(city_data_frame)
        return city_data_frame

    def get_hackney_cases(self, data_frame):
        # print("[get_hackney_cases] Creating Hackney Case Dataframe")
        hack_data_frame = data_frame[data_frame['UTLA'] == 'Hackney']
        hack_data_frame = hack_data_frame[(~hack_data_frame['Phone'].isna()) |
                                          (~hack_data_frame['Phone2'].isna())]
        # ensures there is at least one Phone Number
        hack_data_frame = hack_data_frame[self.COLS]
        return hack_data_frame

    @classmethod
    def get_text_message_list(cls, data_frame):
        # print("[get_text_message_list] Cases with no Phone Number for Text messaging")
        # Phone col appears to be always a mobile
        text_list = data_frame[~data_frame['Phone'].isna()]
        text_list = text_list[['Phone']]
        # print(text_list)
        return text_list

    # Only returns cases that don't have any phone number
    @classmethod
    def get_address_email_lists(cls, data_frame):
        # print(
        #     "[get_address_email_lists] Only returns cases that don't have any phone number")
        address_list = data_frame[(data_frame['House Number'].str.len() > 0)
                                  & (data_frame['Postcode'].str.len() > 0)
                                  & (data_frame['Phone'].str.len() == 0)
                                  & (data_frame['Phone2'].str.len() == 0)]

        address_list = address_list[[
            'Date Time Extracted',
            'Forename',
            'Surname',
            'House Number',
            'Postcode'
        ]]

        email_list = data_frame[
            (data_frame['Email'].str.len() > 0)
            & (data_frame['Phone'].str.len() == 0)
            & (data_frame['Phone2'].str.len() == 0)
            ]
        email_list = email_list[['Date Time Extracted',
                                 'Forename', 'Surname', 'Email']]
        # print(address_list)
        # print(email_list)
        return address_list, email_list

    def clean_data(self, data_frame, excluded_ctas_ids):  # takes whole sheet and lints data
        for i in self.COLS:
            data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'\s+', '')
            data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'nan', np.nan)

        # some account ids are just numbers, we need them to be string
        data_frame['Account ID'] = data_frame['Account ID'].astype(str)

        indexes = []

        for index, row in data_frame.iterrows():
            if not self.is_from_last_fourteen_days(row["Date Tested"]) or row["Account ID"] in excluded_ctas_ids:
                indexes.append(index)

        if len(indexes) > 0:
            print('Warning: Ignored ' + str(
                len(indexes)) + ' contact tracing rows that were older than 14 days or an excluded ctas id.')

        cleaned_data_frame = data_frame.drop(data_frame.index[indexes])

        return cleaned_data_frame

    def is_from_last_fourteen_days(self, date_tested):
        if not date_tested:
            return False

        parsed_tested_date = manual_parse(date_tested)
        today = dt.date.today()

        if (today - parsed_tested_date.date()).days >= 14:
            return False
        else:
            return True
