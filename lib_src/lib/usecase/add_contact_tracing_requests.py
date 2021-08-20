import datetime
from dateutil import parser

from ..helpers import parse_date_of_birth, manual_parse

class AddContactTracingRequests:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request

    def execute(self, data_frame):
        responses = []

        for index, row in data_frame.iterrows():
            if not self.is_from_last_fourteen_days(row):
                continue

            row = row.to_dict()

            dob_day, dob_month, dob_year = parse_date_of_birth(
                row['Date of Birth'])

            metadata = {
                "first_symptomatic_at": row["First Symptomatic At"],
                "date_tested": row["Date Tested"]
            }

            help_request = [
                {
                    "Postcode": row['Postcode'].upper(),
                    "AddressFirstLine": row['House Number'],
                    "HelpWithSomethingElse": True,
                    "FirstName": row["Forename"].capitalize() if row['Forename'] else '',
                    "LastName": row["Surname"].capitalize() if row['Surname'] else '',
                    "DobDay": f'{dob_day}',
                    "DobMonth": f'{dob_month}',
                    "DobYear": f'{dob_year}',
                    "ContactTelephoneNumber":  row["Phone"],
                    "ContactMobileNumber":  row["Phone2"],
                    "EmailAddress":  row["Email"],
                    "CallbackRequired": True,
                    "CaseNotes": row["Comments"],
                    "HelpNeeded": "Contact Tracing",
                    "NhsNumber": row["NHS Number"],
                    "Metadata": metadata,
                    "NhsCtasId": row["Account ID"]
                }
            ]

            responses.append(self.create_help_request.execute(help_requests=help_request))

        return responses

    def is_from_last_fourteen_days(self, row):
        if not row["Date Tested"]:
            return False

        parsed_tested_date = manual_parse(row["Date Tested"])
        today = datetime.date.today()

        if (today - parsed_tested_date.date()).days >= 14:
            return False
        else:
            return True
