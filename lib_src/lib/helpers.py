import datetime
import re

from dateutil import parser
import numpy as np


def manual_parse(date_string):
    date_string = re.sub(r"(\s\d\d:\d\d)(?=$|\s)", "\g<1>:00", date_string)
    date_numbers_string = re.findall(r'\d+', date_string)
    date_numbers_string = [date_portion.zfill(2) for date_portion in date_numbers_string]
    date_numbers_string = ''.join(date_numbers_string)

    try:
        date = datetime.datetime.strptime(date_numbers_string, "%Y%m%d")
        return date
    except ValueError:
        pass

    try:
        date = datetime.datetime.strptime(date_numbers_string, "%d%m%Y")
        return date
    except ValueError:
        pass

    try:
        date = datetime.datetime.strptime(date_numbers_string, "%Y%m%d%H%M%S")
        return date
    except ValueError:
        pass

    return parser.parse(date_string, dayfirst=True)


def parse_date_of_birth(date_of_birth):
    if not date_of_birth:
        return "", "", ""

    parsed_date = manual_parse(date_of_birth)

    dob_day = parsed_date.day
    dob_month = parsed_date.month
    dob_year = parsed_date.year

    return dob_day, dob_month, dob_year


def concatenate_address(address_line_1, house_number):
    if not address_line_1:
        return house_number

    if not house_number:
        return address_line_1

    if house_number == address_line_1:
        return house_number

    return house_number + ' ' + address_line_1


def case_note_needs_an_update(case_notes_on_request, new_case_note):
    if not case_notes_on_request:
        return True
    else:
        for case_note in case_notes_on_request:
            if case_note.get('note', None) == new_case_note:
                return False
        return True


def resident_is_identifiable(help_request):
    try:
        if help_request.get('NhsNumber'):
            return True

        if help_request.get('FirstName') and help_request.get('LastName'):
            match_fields = ['NhsCtasId', 'Uprn', 'ContactTelephoneNumber', 'ContactMobileNumber', 'EmailAddress']

            if all(help_request.get(field) for field in ['DobDay', 'DobMonth', 'DobYear']) or \
                    any(help_request.get(field) for field in match_fields):
                return True

        return False
    except Exception as e:
        print("Helper Error: 'resident_is_identifiable' has encountered unexpected data.", str(e), help_request)
        # Don't want to handle this by returning a bool value as this would imply
        # that resident was not identifiable rather than resident data was unexpected.
        raise e


def clean_data(columns, data_frame):
    for i in columns:
        data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'\s+', '')
        data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'nan', np.nan)

    return data_frame

# No need to test this, as it's basically base python method
def is_within_collection(value, collection):
    return any(item == value for item in collection)