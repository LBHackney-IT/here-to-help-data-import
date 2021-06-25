import datetime
from ..helpers import parse_date_of_birth, case_note_needs_an_update


class AddSelfIsolationRequests:
    def __init__(self, create_help_request, here_to_help_api):
        self.create_help_request = create_help_request
        self.here_to_help_api = here_to_help_api

    def execute(self, data_frame):
        print("add")
        data_frame.insert(0, 'help_request_id', '')
        data_frame.insert(0, 'resident_id', '')

        for index, row in data_frame.iterrows():

            dob_day, dob_month, dob_year = parse_date_of_birth(
                row['Date of Birth'])

            metadata = {
                "LA_support_required": row["LA Support Required"],
                "LA_support_letter_received": row["LA Support Letter Received"]
            }

            help_request = [
                {
                    "Metadata": metadata,
                    "Uprn": row.UPRN,
                    "Postcode": row.Postcode.upper(),
                    "AddressFirstLine": row['Address Line 1'],
                    "AddressSecondLine": row['Address Line 2'],
                    "AddressThirdLine": row.Town,
                    "FirstName": row.Forename.capitalize() if row.Forename else '',
                    "LastName": row.Surname.capitalize() if row.Surname else '',
                    "DobDay": f'{dob_day}',
                    "DobMonth": f'{dob_month}',
                    "DobYear": f'{dob_year}',
                    "ContactTelephoneNumber": row.Phone2,
                    "ContactMobileNumber": row.Phone,
                    "EmailAddress": row.Email,
                    "CallbackRequired": True,
                    "HelpNeeded": "Welfare Call",
                    "NhsNumber": row['NHS Number'],
                    "NhsCtasId": row.ID
                }]
            print(help_request)
            response = self.create_help_request.execute(
                help_requests=help_request)

            if response['created_help_request_ids']:
                help_request_id = response['created_help_request_ids'][0]

                request = self.here_to_help_api.get_help_request(
                    help_request_id)

                resident_id = request["ResidentId"]

                data_frame.at[index, 'help_request_id'] = help_request_id
                data_frame.at[index, 'resident_id'] = resident_id

                print(f'Added CEV {index+1} of {len(data_frame)}: resident_id: {resident_id} help_request_id: {help_request_id}')

                # if case_note_needs_an_update(request['CaseNotes'], nsss_case_note):
                #     self.here_to_help_api.create_case_note(
                #         resident_id, help_request_id, {
                #             "author": author, "note": nsss_case_note})

            return data_frame

    # def is_called_required(self, row):
    #     return True if row['do_you_need_someone_to_contact_you_about_local_support'].lower(
    #     ) == 'yes' else False
    #
    # def get_case_note(self, row):
    #     author = "Data Ingestion: National Shielding Service System"
    #     note_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")
    #     case_note = 'CEV: Dec 2020 Tier 4 '
    #     case_note += f'NSSS Submitted on:  ' + \
    #         str(row['submission_datetime']) + '. '
    #     case_note += 'Do you want supermarket deliveries? ' + \
    #         row['do_you_want_supermarket_deliveries'] + '. '
    #     case_note += 'Do you have someone to go shopping for you? ' + row[
    #         'do_you_have_someone_to_go_shopping_for_you'] + '. '
    #     case_note += 'Do you need someone to contact you about local support? ' + \
    #         row['do_you_need_someone_to_contact_you_about_local_support'] + '.'
    #
    #     return author, note_date, case_note
