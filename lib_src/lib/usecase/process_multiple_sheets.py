import datetime as dt


class ProcessMultipleSheets:

    def __init__(self, google_drive_gateway, pygsheet_gateway):
        self.google_drive_gateway = google_drive_gateway
        self.pygsheet_gateway = pygsheet_gateway

    def execute(self, inbound_folder_id, outbound_folder_id, data_processor):
        inbound_files = self.google_drive_gateway.get_list_of_files(
            inbound_folder_id)
        if not inbound_files:
            print(
                "No File found for today in folder: https://drive.google.com/drive/folders/%s " %
                (inbound_folder_id))
            print("Will Abort")
            return 'not found'

        outbound_files = self.google_drive_gateway.get_list_of_files(
            outbound_folder_id)

        if len(inbound_files) == len(outbound_files):
            print(
                "Output file found in output folder: https://drive.google.com/drive/folders/%s " %
                (outbound_folder_id))
            print("Will Abort")
            return 'all done'

        for file in inbound_files:
            today = dt.datetime.now().date().strftime('%Y-%m-%d')

            processed_file_name = f'PROCESSED_{file.get("name")}_{today}'

            if not any(
                    f['name'] == processed_file_name for f in outbound_files):
                print(
                    f'processing {len(outbound_files) + 1} of {len(inbound_files)}')

                inbound_spread_sheet_id = file.get('id')

                data_frame = self.pygsheet_gateway.get_data_frame_from_sheet(
                    inbound_spread_sheet_id, 'A1')

                processed_data_frame = data_processor.execute(data_frame)

                output = [{
                    'sheet_title': 'hackney_cases',
                    'data_frame': processed_data_frame
                }]

                hackney_output_spreadsheet_key = self.google_drive_gateway.create_spreadsheet(
                    outbound_folder_id, processed_file_name)

                self.pygsheet_gateway.populate_spreadsheet(
                    output, spreadsheet_key=hackney_output_spreadsheet_key)

                break
