import datetime as dt
class FindAndProcessNewSheet:

    def __init__(self, google_drive_gateway, gspread_drive_gateway):
        self.google_drive_gateway = google_drive_gateway
        self.gspread_drive_gateway = gspread_drive_gateway

    def execute(self, inbound_folder_id, outbound_folder_id ):
        today = dt.datetime.now().date().strftime('%Y-%m-%d')

        print("[CheckLogic: %s] Begin Check" % dt.datetime.now())

        if self.google_drive_gateway.searchFolder(inbound_folder_id, today, "spreadsheet") == True:
            if self.google_drive_gateway.searchFolder(outbound_folder_id, today, "spreadsheet") == False:
                print("[CheckLogic: %s] Run DataWrangleScript" % dt.datetime.now())
                foundFileID = self.google_drive_gateway.getFile(inbound_folder_id, today, "spreadsheet")
                print(foundFileID)

                df = self.gspread_drive_gateway.get_cases_from_gsheet(foundFileID)
                city_cases = self.gspread_drive_gateway.get_city_cases(df=df)
                hackney_cases = self.get_hackney_cases(df=df)
                text_list = self.get_text_message_list(df=hackney_cases)
                address_list, email_list = self.get_address_email_lists(df=hackney_cases)
                city_dfs = [[city_cases, 'city_cases']]
                output_dfs = [[email_list, 'email_list'], [address_list, 'address_list'],
                              [hackney_cases, 'hackney_cases']]
                self.gspread_drive_gateway.create_output_spreadsheet(data_frame=output_dfs, outbound_folder_id=outbound_folder_id)
                self.gspread_drive_gateway.create_city_spreadsheet(data_frame=city_dfs, outbound_folder_id=outbound_folder_id)
                cases_dict = self.hackney_cases_to_dict(df=hackney_cases)
                print(cases_dict)

            else:
                print(
                    "[CheckLogic: %s] A file has been found in the output folder: https://drive.google.com/drive/folders/%s " % (
                    dt.datetime.now(), outbound_folder_id))
                print("[CheckLogic: %s] Will Abort")
        else:
            print(
                "[CheckLogic: %s] No File found for todays PowerBI Output in folder: https://drive.google.com/drive/folders/%s " % (
                dt.datetime.now(), inbound_folder_id))
            print("[CheckLogic: %s] Will Abort" % dt.datetime.now())

    # results = drive_service.files().list(supportsAllDrives=True, includeItemsFromAllDrives=True, q="parents in '{folder_id}' and trashed = false", fields = "nextPageToken, files(id, name)").execute()

    # q: mimeType = 'application/vnd.google-apps.folder'

    def get_city_cases(self, df):
        print("[get_city_cases] Creating COL Case Dataframe")
        city_df = df[df['UTLA'] == 'City of London']
        print(city_df)
        return city_df

    def get_hackney_cases(self, df):
        print("[get_hackney_cases] Creating Hackney Case Dataframe")
        hack_df = df[df['UTLA'] == 'Hackney']
        hack_df = hack_df[(~hack_df['Phone'].isna()) | (~hack_df['Phone2'].isna())]
        # ensures there is at least one Phone Number
        hack_df = hack_df[self.gspread_drive_gateway.COLS]
        return hack_df

    def get_text_message_list(self, df):
        print("[get_text_message_list] Cases with no Phone Number for Text messaging")
        text_list = df[~df['Phone'].isna()]  # Phone col appears to be always a mobile
        text_list = text_list[['Phone']]
        # print(text_list)
        return text_list

    def get_address_email_lists(self, df):  # Only returns cases that don't have any phone number
        print("[get_address_email_lists] Only returns cases that don't have any phone number")
        address_list = df[
            (df['House Number'].str.len() > 0) & (df['Postcode'].str.len() > 0) & (df['Phone'].str.len() == 0) & (
                    df['Phone2'].str.len() == 0)]
        address_list = address_list[['Date Time Extracted', 'Forename', 'Surname', 'House Number', 'Postcode']]
        email_list = df[(df['Email'].str.len() > 0) & (df['Phone'].str.len() == 0) & (df['Phone2'].str.len() == 0)]
        email_list = email_list[['Date Time Extracted', 'Forename', 'Surname', 'Email']]
        # print(address_list)
        # print(email_list)
        return address_list, email_list

    def hackney_cases_to_dict(self, df):
        """
        df: (dataframe)
        returns:

        """
        cases_dict = df.to_dict(orient="records")
        return cases_dict
