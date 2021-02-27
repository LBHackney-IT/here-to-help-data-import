import datetime as dt
from ..helpers import clean_data, print_log

class ProcessSPLCalls:
    COLS = [
        'Traced_NHSNUMBER',
        'PatientFirstName',
        'PatientOtherName',
        'PatientSurname',
        'DateOfBirth',
        'PatientAddress_Line1',
        'PatientAddress_Line2',
        'PatientAddress_Line3',
        'PatientAddress_Line4',
        'PatientAddress_Line5',
        'PatientAddress_PostCode',
        'PatientEmailAddress',
        'mobile',
        'landline',
        'DateOfDeath',
        'Flag_PDSInformallyDeceased',
        'oslaua',
        'oscty',
        'Data_Source',
        'category',
        'InceptionDate',
        'SPL_Version',
        'uprn'
    ]

    def __init__(self, google_drive_gateway, pygsheet_gateway, add_spl_requests):
        self.google_drive_gateway = google_drive_gateway
        self.pygsheet_gateway = pygsheet_gateway
        self.add_spl_requests = add_spl_requests

    def execute(self, inbound_folder_id, outbound_folder_id):
        inbound_spread_sheet_id = self.google_drive_gateway.search_folder(
                inbound_folder_id, "spreadsheet")

        return_log = []

        if inbound_spread_sheet_id:
            if not self.google_drive_gateway.search_folder(
                    outbound_folder_id, "spreadsheet"):

                data_frame = self.pygsheet_gateway.get_data_frame_from_sheet(
                    inbound_spread_sheet_id, 'A1')

                data_frame = clean_data(columns=self.COLS, data_frame=data_frame)

                processed_data_frame = self.add_spl_requests.execute(data_frame)

                output = [{
                    'sheet_title': 'hackney_cases',
                    'data_frame': processed_data_frame
                }]

                today = dt.datetime.now().date().strftime('%Y-%m-%d')

                output_file_name = f'Hackney_SPL_CASES_{today}'

                hackney_output_spreadsheet_key = self.google_drive_gateway.create_spreadsheet(
                    outbound_folder_id, output_file_name)

                print(f'{len(processed_data_frame)} records processed and saved in {output_file_name}')

                self.pygsheet_gateway.populate_spreadsheet(
                    output, spreadsheet_key=hackney_output_spreadsheet_key)
            else:
                return_log.append(print_log("SPL output file found in output folder: https://drive.google.com/drive/folders/%s" %(outbound_folder_id)))
                return_log.append(print_log("Will Abort"))
        else:
            return_log.append(print_log(
                "No File new file was found SPL inbound folder: https://drive.google.com/drive/folders/%s " %(inbound_folder_id)))
            return_log.append(print_log("Will Abort"))

        return return_log
