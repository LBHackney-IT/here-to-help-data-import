from dateutil import parser
import numpy as np


def parse_date_of_birth(date_of_birth):
    dob_day = parser.parse(
        date_of_birth,
        dayfirst=True).day if date_of_birth else ''
    dob_month = parser.parse(
        date_of_birth,
        dayfirst=True).month if date_of_birth else ''
    dob_year = parser.parse(
        date_of_birth,
        dayfirst=True).year if date_of_birth else ''

    return dob_day, dob_month, dob_year


def clean_data(columns, data_frame):
    for i in columns:
        data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'\s+', '')
        data_frame[i] = data_frame[i].astype(str).str.strip().replace(r'nan', np.nan)

    return data_frame
