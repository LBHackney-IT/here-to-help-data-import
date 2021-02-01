from dateutil import parser

class AddHackneyCasesToApp:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request

    def execute(self, data_frame):
        responses = []

        for index, row in data_frame.iterrows():
            row = row.to_dict()

            help_request = [
                {
                    "Postcode": row['Postcode'].upper(),
                    "AddressFirstLine": row['House Number'],
                    "HelpWithSomethingElse": True,
                    "FirstName": row["Forename"].capitalize() if row['Forename'] else '',
                    "LastName": row["Surname"].capitalize() if row['Surname'] else '',
                    "DobDay": parser.parse(row['Date of Birth'], dayfirst=True).day if row['Date of Birth'] else '',
                    "DobMonth": parser.parse(row['Date of Birth'], dayfirst=True).month if row['Date of Birth'] else '',
                    "DobYear": parser.parse(row['Date of Birth'], dayfirst=True).year if row['Date of Birth'] else '',
                    "ContactTelephoneNumber":  row["Phone"],
                    "ContactMobileNumber":  row["Phone2"],
                    "EmailAddress":  row["Email"],
                    "CallbackRequired": True,
                    "CaseNotes": row["Comments"],
                    "HelpNeeded": "Contact Tracing",
                    "NhsNumber": row["NHS Number"],
                    "NhsCtasId": row["Account ID"].upper()
                }
            ]

            responses.append(self.create_help_request.execute(help_requests=help_request))

        return responses
