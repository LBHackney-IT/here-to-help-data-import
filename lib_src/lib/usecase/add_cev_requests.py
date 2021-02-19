from dateutil import parser
import datetime


class AddCEVRequests:
    def __init__(self, create_help_request, here_to_help_api):
        self.create_help_request = create_help_request
        self.here_to_help_api = here_to_help_api

    def execute(self, data_frame):
        data_frame.insert(0, 'help_request_id', '')

        for index, row in data_frame.iterrows():

            dob_day = parser.parse(
                row.date_of_birth,
                dayfirst=True).day if row.date_of_birth else ''
            dob_month = parser.parse(
                row.date_of_birth,
                dayfirst=True).month if row.date_of_birth else ''
            dob_year = parser.parse(
                row.date_of_birth,
                dayfirst=True).year if row.date_of_birth else ''

            metadata = {
                "nsss_id": row["ID"]
            }

            author, note_date, nsss_case_note = self.get_case_note(row)

            help_request = [
                {
                    "Metadata": metadata,
                    "Uprn": row.address_uprn,
                    "Postcode": row.address_postcode.upper(),
                    "AddressFirstLine": row.address_line1,
                    "AddressSecondLine": row.address_line2,
                    "AddressThirdLine": row.address_town_city,
                    "CaseNotes": f'{{"author":"{author}","noteDate":" {note_date}","note":"{nsss_case_note}"}}',
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
                    "NhsNumber": row.nhs_number}]

            response = self.create_help_request.execute(
                help_requests=help_request)

            if response['created_help_request_ids']:
                help_request_id = response['created_help_request_ids'][0]

                data_frame.at[index, 'help_request_id'] = help_request_id
                request = self.here_to_help_api.get_help_request(
                    help_request_id)

                if not any(
                        case_note['note'] == nsss_case_note for case_note in request['CaseNotes']):
                    resident_id = request["ResidentId"]
                    self.here_to_help_api.create_case_note(
                        resident_id, help_request_id, {"author": author,"noteDate": note_date,"note":nsss_case_note})

        return data_frame

    def is_called_required(self, row):
        return True if row['do_you_need_someone_to_contact_you_about_local_support'].lower(
        ) == 'yes' else False

    def get_case_note(self, row):
        author = "Data Ingestion: National Shielding Service System list"
        note_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")
        case_note = 'CEV: Dec 2020 Tier 4 '
        case_note += f'NSSS Submitted on:  ' + \
            str(row['submission_datetime']) + '. '
        case_note += 'Do you want supermarket deliveries? ' + \
            row['do_you_want_supermarket_deliveries'] + '. '
        case_note += 'Do you have someone to go shopping for you? ' + row[
            'do_you_have_someone_to_go_shopping_for_you'] + '. '
        case_note += 'Do you need someone to contact you about local support? ' + \
            row['do_you_need_someone_to_contact_you_about_local_support'] + '.'

        return author, note_date, case_note
