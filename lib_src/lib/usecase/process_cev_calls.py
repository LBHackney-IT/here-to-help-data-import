import datetime as dt
import numpy as np

class ProcessCevCalls:
    COLS = [
        'nhs_number',
        # 'ID',
        'first_name',
        # 'middle_name',
        'last_name',
        'date_of_birth',
        'address_line1',
        'address_line2',
        'address_town_city',
        'address_postcode',
        'address_uprn',
        'contact_number_calls',
        'contact_number_texts',
        'contact_email',
        # 'uid_submission',
        # 'submission_datetime',
        # 'are_you_applying_on_behalf_of_someone_else',
        # 'have_you_received_an_nhs_letter',
        'do_you_want_supermarket_deliveries',
        'do_you_need_someone_to_contact_you_about_local_support',
        # 'do_you_have_one_of_the_listed_medical_conditions',
        # 'do_you_have_someone_to_go_shopping_for_you',
        # 'ladcode',
        # 'active_status',
        # 'spl_category',
        # 'spl_address_line1',
        # 'spl_address_line2',
        # 'spl_address_line3',
        # 'spl_address_line4',
        # 'spl_address_line5',
        # 'spl_address_postcode',
        # 'spl_address_uprn',
        # 'help_request_id'
    ]

    def __init__(self, google_drive_gateway, pygsheet_gateway, add_cev_requests):
        self.google_drive_gateway = google_drive_gateway
        self.pygsheet_gateway = pygsheet_gateway
        self.add_cev_requests = add_cev_requests

    def execute(self, inbound_folder_id, outbound_folder_id):
        inbound_spread_sheet_id = self.google_drive_gateway.search_folder(
                inbound_folder_id, "spreadsheet")

        if inbound_spread_sheet_id:
            if not self.google_drive_gateway.search_folder(
                    outbound_folder_id, "spreadsheet"):

                data_frame = self.pygsheet_gateway.get_data_frame_from_sheet(
                    inbound_spread_sheet_id, 'A1')

                data_frame = self.clean_data(data_frame=data_frame)

                processed_data_frame = self.add_cev_requests.execute(data_frame)

                output = [{
                    'sheet_title': 'hackney_cases',
                    'data_frame': processed_data_frame
                }]

                today = dt.datetime.now().date().strftime('%Y-%m-%d')

                hackney_output_spreadsheet_key = self.google_drive_gateway.create_spreadsheet(
                    outbound_folder_id, f'Hackney_NSSS_CASES_{today}')

                self.pygsheet_gateway.populate_spreadsheet(
                    output, spreadsheet_key=hackney_output_spreadsheet_key)

            else:
                print(
                    "NSSS output file found in \
                    output folder: https://drive.google.com/drive/folders/%s " %
                    (outbound_folder_id))
                print("Will Abort")
        else:
            print(
                "No File found for todays NSSS Output in \
                folder: https://drive.google.com/drive/folders/%s " %
                (inbound_folder_id))
            print("Will Abort")

    def clean_data(self, data_frame):
        for i in self.COLS:
            data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'\s+', '')
            data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'nan', np.nan)

        return data_frame
