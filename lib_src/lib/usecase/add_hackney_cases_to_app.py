class AddHackneyCasesToApp:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request

    def execute(self, data_frame):
        responses = []

        for index, row in data_frame.iterrows():
            row = row.to_dict()

            dob = row['Date of Birth'].split('-')

            dob_day = dob[0] if row['Date of Birth'] else ''
            dob_month = dob[1] if row['Date of Birth'] else ''
            dob_year = dob[2] if row['Date of Birth'] else ''

            help_request = [
                {
                    "Postcode": row['Postcode'].upper(),
                    "AddressFirstLine": row['House Number'],
                    "HelpWithSomethingElse": True,
                    "FirstName": row["Forename"].capitalize() if row['Forename'] else '',
                    "LastName": row["Surname"].capitalize() if row['Surname'] else '',
                    "DobDay": dob_day,
                    "DobMonth": dob_month,
                    "DobYear": dob_year,
                    "ContactTelephoneNumber":  row["Phone"],
                    "ContactMobileNumber":  row["Phone2"],
                    "EmailAddress":  row["Email"],
                    "CallbackRequired": True,
                    "CaseNotes": row["Comments"],
                    "HelpNeeded": "Contact Tracing",
                    "NhsNumber": row["NHS Number"],
                    "NhsCtasId": row["Account ID"]
                }
            ]

            responses.append(self.create_help_request.execute(help_requests=help_request))

        return responses
