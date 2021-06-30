import datetime
from ..helpers import parse_date_of_birth, case_note_needs_an_update, concatenate_address


class AddSelfIsolationRequests:
    def __init__(self, create_help_request, here_to_help_api):
        self.create_help_request = create_help_request
        self.here_to_help_api = here_to_help_api

    def execute(self, data_frame):
        print("add")
        data_frame.insert(0, 'help_request_id', '')
        data_frame.insert(0, 'resident_id', '')

        for index, row in data_frame.iterrows():
            if not self.is_self_isolation_request(row):
                continue

            dob_day, dob_month, dob_year = parse_date_of_birth(
                row['Date of Birth'])

            address_line_1 = concatenate_address(row['Address Line 1'], row['House Number'])

            metadata = {
                "LA_support_required": row["LA Support Required"],
                "LA_support_letter_received": row["LA Support Letter Received"]
            }

            help_request = [
                {
                    "Metadata": metadata,
                    "Uprn": row.UPRN,
                    "Postcode": row.Postcode.upper(),
                    "AddressFirstLine": address_line_1,
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

                print(
                    f'Added CEV {index + 1} of {len(data_frame)}: resident_id: {resident_id} help_request_id: {help_request_id}')

        return data_frame

    def is_self_isolation_request(self, row):
        return True if row["LA Support Required"] == '1' or row["LA Support Letter Received"] == "1" else False
