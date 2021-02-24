from dateutil import parser

from ..helpers import parse_date_of_birth

class AddContactTracingRequests:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request

    def execute(self, data_frame):
        responses = []

        for index, row in data_frame.iterrows():
            row = row.to_dict()

            dob_day, dob_month, dob_year = parse_date_of_birth(
                row['Date of Birth'], day_first=True)

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
