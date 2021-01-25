import datetime as dt


class FindAndProcessNewSheet:

    def __init__(self, google_drive_gateway, gspread_drive_gateway, add_hackney_cases_to_app):
        self.google_drive_gateway = google_drive_gateway
        self.gspread_drive_gateway = gspread_drive_gateway
        self.add_hackney_cases_to_app = add_hackney_cases_to_app

    def execute(self, inbound_folder_id, outbound_folder_id):
        today = dt.datetime.now().date().strftime('%Y-%m-%d')

        # print("[CheckLogic: %s] Begin Check" % dt.datetime.now())

        if self.google_drive_gateway.search_folder(
                inbound_folder_id, today, "spreadsheet"):
            if not self.google_drive_gateway.search_folder(
                    outbound_folder_id, today, "spreadsheet"):
                # print(
                #     "[CheckLogic: %s] Run DataWrangleScript" %
                #     dt.datetime.now())
                found_file_id = self.google_drive_gateway.get_file(
                    inbound_folder_id, today, "spreadsheet")
                # print(found_file_id)

                data_frame = self.gspread_drive_gateway.get_cases_from_gsheet(
                    found_file_id)
                city_cases = self.get_city_cases(data_frame=data_frame)
                hackney_cases = self.get_hackney_cases(data_frame=data_frame)
                # text_list = self.get_text_message_list(data_frame=hackney_cases)
                address_list, email_list = self.get_address_email_lists(
                    data_frame=hackney_cases)
                city_data_frames = [[city_cases, 'city_cases']]
                output_data_frames = [[email_list, 'email_list'], [
                    address_list, 'address_list'], [hackney_cases, 'hackney_cases']]
                print('--  --  start adding to api --  --  --  --  --')
                self.add_hackney_cases_to_app.execute(hackney_cases)
                print('--  --  send adding to api --  --  --  --  -- ')
                self.gspread_drive_gateway.create_output_spreadsheet(
                    data_frame=output_data_frames, outbound_folder_id=outbound_folder_id)
                self.gspread_drive_gateway.create_city_spreadsheet(
                    data_frame=city_data_frames, outbound_folder_id=outbound_folder_id)
                # cases_dict = self.hackney_cases_to_dict(data_frame=hackney_cases)
                # print(cases_dict)

            else:
                print(
                    "[CheckLogic: %s] A file has been found in the \
                    output folder: https://drive.google.com/drive/folders/%s " %
                    (dt.datetime.now(), outbound_folder_id))
                print("[CheckLogic: %s] Will Abort")
        else:
            print(
                "[CheckLogic: %s] No File found for todays PowerBI Output in \
                folder: https://drive.google.com/drive/folders/%s " %
                (dt.datetime.now(), inbound_folder_id))
            print("[CheckLogic: %s] Will Abort" % dt.datetime.now())

    # results =
    #   drive_service.files().list(supportsAllDrives=True,
    #   includeItemsFromAllDrives=True,
    #   q="parents in '{folder_id}' and trashed = false",
    #   fields = "nextPageToken, files(id, name)").execute()

    # q: mimeType = 'application/vnd.google-apps.folder'

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
        hack_data_frame = hack_data_frame[self.gspread_drive_gateway.COLS]
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
        address_list =  data_frame[(data_frame['House Number'].str.len() > 0)
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

    @classmethod
    def hackney_cases_to_dict(cls, data_frame):
        """
        data_frame: (dataframe)
        returns:

        """
        cases_dict = data_frame.to_dict(orient="records")
        return cases_dict
