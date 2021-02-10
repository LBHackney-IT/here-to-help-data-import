from dateutil import parser


class AddCEVRequests:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request

    def execute(self, data_frame):
        data_frame.insert(0, 'help_request_id', '')

        for index, row in data_frame.iterrows():

            dob_day = parser.parse(row.date_of_birth, dayfirst=True).day if row.date_of_birth else ''
            dob_month = parser.parse(row.date_of_birth, dayfirst=True).month if row.date_of_birth else ''
            dob_year = parser.parse(row.date_of_birth, dayfirst=True).year if row.date_of_birth else ''

            # metadata = {
            #     "first_symptomatic_at": row["First Symptomatic At"],
            #     "date_tested": row["Date Tested"]
            # }

            help_request = [
                {
                    # "Metadata": metadata,
                    "Uprn": row.address_uprn,
                    "Postcode": row.address_postcode.upper(),
                    "AddressFirstLine": row.address_line1,
                    "AddressSecondLine": row.address_line2,
                    "AddressThirdLine": row.address_town_city,
                    "CaseNotes": "Imported from National Shielding Service System list",
                    "HelpWithAccessingSupermarketFood": self.help_needed_with_supermarket_deliveries(row),
                    "HelpWithSomethingElse": True,
                    "FirstName": row.first_name.capitalize() if row.first_name else '',
                    "LastName": row.last_name.capitalize() if row.last_name else '',
                    "DobDay": f'{dob_day}',
                    "DobMonth": f'{dob_month}',
                    "DobYear": f'{dob_year}',
                    "ContactTelephoneNumber": row.contact_number_calls,
                    "ContactMobileNumber": row.contact_number_texts,
                    "EmailAddress": row.contact_email,
                    "CallbackRequired": self.is_called_required(row),
                    "HelpNeeded": "Shielding",
                    "NhsNumber": row.nhs_number
                }
            ]

            response = self.create_help_request.execute(help_requests=help_request)

            if response['created_help_request_ids']:
                data_frame.at[index, 'help_request_id'] = response['created_help_request_ids'][0]

        return data_frame

    def is_called_required(self, row):
        return True if row['do_you_need_someone_to_contact_you_about_local_support'].lower() == 'yes' else False

    def help_needed_with_supermarket_deliveries(self, row):
        return True if row['do_you_want_supermarket_deliveries'].lower() == 'yes' else False
