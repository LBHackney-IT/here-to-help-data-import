import datetime
import re

from dateutil import parser
import numpy as np


def manual_parse(date_string):
    date_numbers_string = re.findall(r'\d+', date_string)
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


def clean_data(columns, data_frame):
    for i in columns:
        data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'\s+', '')
        data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'nan', np.nan)

    return data_frame
