import datetime
from .helpers import parse_date_of_birth


class AddSPLRequests:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request

    def execute(self, data_frame):
        data_frame.insert(0, 'help_request_id', '')

        for index, row in data_frame.iterrows():

            dob_day, dob_month, dob_year = parse_date_of_birth(
                row.DateOfBirth, year_first=True)

            metadata = {
                "spl_id": row.Traced_NHSNUMBER
            }

            author, note_date, nsss_case_note = self.get_case_note(row)

            help_request = [
                {
                    "Metadata": metadata,
                    "Uprn": row.uprn,
                    "Postcode": row.PatientAddress_PostCode.upper(),
                    "AddressFirstLine": row.PatientAddress_Line1,
                    "AddressSecondLine": row.PatientAddress_Line2,
                    "AddressThirdLine": row.PatientAddress_Line3,
                    "CaseNotes": f'{{"author":"{author}","noteDate":" {note_date}","note":"{nsss_case_note}"}}',
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

            if response['created_help_request_ids']:
                help_request_id = response['created_help_request_ids'][0]

                data_frame.at[index, 'help_request_id'] = help_request_id

        return data_frame

    def get_case_note(self, row):
        author = "Data Ingestion: Shielding Patient List"
        note_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")
        case_note = f'SPL Category: {row.category}.'

        if row.DateOfDeath:
            case_note += f' Date of death: {row.DateOfDeath}'

        return author, note_date, case_note
