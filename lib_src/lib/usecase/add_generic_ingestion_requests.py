import datetime
from ..helpers import parse_date_of_birth

valid_help_request_types = {
    "EUSS": "EUSS",
    "LINK WORK": "Link Work"
}

valid_help_request_subtypes = {
    "REPAIRS": "Repairs"
}


class AddGenericIngestionRequests:
    def __init__(self, create_help_request, here_to_help_api):
        self.create_help_request = create_help_request
        self.here_to_help_api = here_to_help_api

    def execute(self, data_frame):
        author = "Data Ingestion: Generic Ingestion"

        data_frame.insert(0, 'help_request_id', '')
        data_frame.insert(0, 'resident_id', '')

        for index, row in data_frame.iterrows():
            help_request_type_upper = row['Help Request Type'].upper() if row['Help Request Type'] else ''
            help_request_subtype_upper = row['Subtype'].upper() if row['Subtype'] else ''

            help_request_type = valid_help_request_types.get(help_request_type_upper)
            help_request_subtype = valid_help_request_subtypes.get(help_request_subtype_upper)

            if not help_request_type:
                continue

            if help_request_subtype is not None and help_request_type == 'EUSS':
                continue

            if help_request_subtype is None:
                help_request_subtype = ''
                print('help_request_subtype',
                      help_request_subtype)

            dob_day, dob_month, dob_year = parse_date_of_birth(
                row['d.o.b'])

            metadata = {
                "Author": author,
                "generic_ingestion_id": help_request_type.replace(" ", "") + help_request_subtype.replace(" ", "")
            }

            help_request = [
                {
                    "Metadata": metadata,
                    "Postcode": row.Postcode.upper(),
                    "Uprn": row['UPRN'],
                    "AddressFirstLine": row['Address Line 1'],
                    "AddressSecondLine": row['Address Line 2'],
                    "AddressThirdLine": row.City,
                    "FirstName": row['First name'].capitalize() if row['First name'] else '',
                    "LastName": row['Surname'].capitalize() if row['Surname'] else '',
                    "DobDay": f'{dob_day}',
                    "DobMonth": f'{dob_month}',
                    "DobYear": f'{dob_year}',
                    "ContactTelephoneNumber": row['Phone number'],
                    "ContactMobileNumber": row['Phone number 2'],
                    "EmailAddress": row.Email if '@' in row.Email else '',
                    "CallbackRequired": True,
                    "HelpNeeded": help_request_type,
                    "HelpNeededSubtype": help_request_subtype
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
                    f'Added Generic Ingestion record of type {help_request_type} {help_request_subtype} {index + 1} of {len(data_frame)}: resident_id: {resident_id} help_request_id: {help_request_id}')

        return data_frame
