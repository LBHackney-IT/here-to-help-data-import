import datetime
from ..helpers import parse_date_of_birth


def is_valid_help_request_type(help_request_type):
    return help_request_type == 'EUSS'


class AddGenericIngestionRequests:
    def __init__(self, create_help_request, here_to_help_api):
        self.create_help_request = create_help_request
        self.here_to_help_api = here_to_help_api

    def execute(self, data_frame):
        author = "Data Ingestion: Generic Ingestion"

        data_frame.insert(0, 'help_request_id', '')
        data_frame.insert(0, 'resident_id', '')

        for index, row in data_frame.iterrows():
            help_request_type = row['Help Request Type']

            if not is_valid_help_request_type(help_request_type):
                continue

            dob_day, dob_month, dob_year = parse_date_of_birth(
                row['d.o.b'])

            metadata = {
                "Author": author,
                "generic_ingestion_id": help_request_type.replace(" ", "")
            }

            help_request = [
                {
                    "Metadata": metadata,
                    "Postcode": row.Postcode.upper(),
                    "AddressFirstLine": row['Address Line 1'],
                    "AddressSecondLine": row['Address Line 2'],
                    "AddressThirdLine": row.City,
                    "FirstName": row['First name'].capitalize() if row['First name'] else '',
                    "LastName": row['Surname'].capitalize() if row['Surname'] else '',
                    "DobDay": f'{dob_day}',
                    "DobMonth": f'{dob_month}',
                    "DobYear": f'{dob_year}',
                    "ContactTelephoneNumber": row['Phone number'],
                    "EmailAddress": row.Email if '@' in row.Email else '',
                    "CallbackRequired": True,
                    "HelpNeeded": help_request_type
                }]

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
                    f'Added Generic Ingestion record of type {help_request_type} {index + 1} of {len(data_frame)}: resident_id: {resident_id} help_request_id: {help_request_id}')

        return data_frame
