from ..helpers import parse_date_of_birth


class AddSPLRequests:
    def __init__(self, create_help_request, here_to_help_api):
        self.create_help_request = create_help_request
        self.here_to_help_api = here_to_help_api

    def execute(self, data_frame):
        data_frame.insert(0, 'help_request_id', '')
        data_frame.insert(0, 'resident_id', '')

        for index, row in data_frame.iterrows():

            dob_day, dob_month, dob_year = parse_date_of_birth(
                row.DateOfBirth, year_first=True)

            metadata = {
                "spl_id": row.Traced_NHSNUMBER
            }

            help_request = [
                {
                    "Metadata": metadata,
                    "Uprn": row.uprn,
                    "Postcode": row.PatientAddress_PostCode.upper(),
                    "AddressFirstLine": row.PatientAddress_Line1,
                    "AddressSecondLine": row.PatientAddress_Line2,
                    "AddressThirdLine": row.PatientAddress_Line3,
                    "HelpWithSomethingElse": True,
                    "FirstName": row.PatientFirstName.capitalize() if row.PatientFirstName else '',
                    "LastName": row.PatientSurname.capitalize() if row.PatientSurname else '',
                    "DobDay": f'{dob_day}',
                    "DobMonth": f'{dob_month}',
                    "DobYear": f'{dob_year}',
                    "ContactTelephoneNumber": row.landline,
                    "ContactMobileNumber": row.mobile,
                    "EmailAddress": row.PatientEmailAddress,
                    "CallbackRequired": False,
                    "HelpNeeded": "Shielding",
                    "NhsNumber": row.Traced_NHSNUMBER}]

            response = self.create_help_request.execute(
                help_requests=help_request)

            author, spl_case_note = self.get_case_note(row)

            if response['created_help_request_ids']:
                help_request_id = response['created_help_request_ids'][0]

                data_frame.at[index, 'help_request_id'] = help_request_id

                request = self.here_to_help_api.get_help_request(
                    help_request_id)

                resident_id = request["ResidentId"]
                data_frame.at[index, 'resident_id'] = resident_id

                if not any(
                        case_note['note'] == spl_case_note for case_note in request['CaseNotes']):
                    resident_id = resident_id
                    self.here_to_help_api.create_case_note(
                        resident_id, help_request_id, {
                            "author": author, "note": spl_case_note})

                    # "CaseNotes": f'{{"author":"{author}","noteDate":" {note_date}","note":"{nsss_case_note}"}}',

        return data_frame

    def get_case_note(self, row):
        author = "Data Ingestion: Shielding Patient List"
        case_note = f'SPL Category: {row.category}.'

        if row.DateOfDeath:
            case_note += f' Date of death: {row.DateOfDeath}'

        return author, case_note
