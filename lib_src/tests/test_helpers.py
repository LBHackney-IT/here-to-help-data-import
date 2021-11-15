import datetime
from faker import Faker
from lib_src.lib.helpers import parse_date_of_birth, case_note_needs_an_update, resident_is_identifiable, manual_parse
from lib_src.lib.helpers import concatenate_address

class TestAddressConcatenation:

    def test_ignores_duplicate_values(self):
        assert concatenate_address('123', '123') == '123'

    def test_concatenates_house_number_with_address_line_1(self):
        assert concatenate_address('A road', '12') == '12 A road'

    def test_ignores_empty_value(self):
        assert concatenate_address('A road', '') == 'A road'
        assert concatenate_address('', '12') == '12'


class TestParseDateOfBirth:

    def test_year_first_no_separators(self):
        test_date = '19830502'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date)

        assert dob_day == 2
        assert dob_month == 5
        assert dob_year == 1983

    def test_recent_year_first_no_separators(self):
        test_date = '20020220'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date)

        assert dob_day == 20
        assert dob_month == 2
        assert dob_year == 2002

    def test_recent_day_first_no_separators(self):
        test_date = '20122013'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date)

        assert dob_day == 20
        assert dob_month == 12
        assert dob_year == 2013

    def test_year_first_with_separators(self):
        test_date = '1983-05-02'
        dob_day, dob_month, dob_year = parse_date_of_birth(test_date)

        assert dob_day == 2
        assert dob_month == 5
        assert dob_year == 1983

    def test_day_first_with_slash_separators(self):
        dob_day, dob_month, dob_year = parse_date_of_birth(
            '03/10/1989')

        assert dob_day == 3
        assert dob_month == 10
        assert dob_year == 1989

    def test_single_digit_month_values(self):
        dob_day, dob_month, dob_year = parse_date_of_birth(
            '25/6/2021')

        assert dob_day == 25
        assert dob_month == 6
        assert dob_year == 2021

    def test_single_day_values(self):
        dob_day, dob_month, dob_year = parse_date_of_birth(
            '2/06/2021')

        assert dob_day == 2
        assert dob_month == 6
        assert dob_year == 2021

    def test_single_month_and_day_values(self):
        dob_day, dob_month, dob_year = parse_date_of_birth(
            '2/6/2021')

        assert dob_day == 2
        assert dob_month == 6
        assert dob_year == 2021

    def test_a_range_of_date_values(self):
        dob_day, dob_month, dob_year = parse_date_of_birth(
            '2/6/2021')

        assert dob_day == 2
        assert dob_month == 6
        assert dob_year == 2021

        dob_day, dob_month, dob_year = parse_date_of_birth(
            '12/6/2021')

        assert dob_day == 12
        assert dob_month == 6
        assert dob_year == 2021

        dob_day, dob_month, dob_year = parse_date_of_birth(
            '13/12/2021')

        assert dob_day == 13
        assert dob_month == 12
        assert dob_year == 2021

        dob_day, dob_month, dob_year = parse_date_of_birth(
            '13/3/2033')

        assert dob_day == 13
        assert dob_month == 3
        assert dob_year == 2033

        dob_day, dob_month, dob_year = parse_date_of_birth(
            '7-3-2033')

        assert dob_day == 7
        assert dob_month == 3
        assert dob_year == 2033

        dob_day, dob_month, dob_year = parse_date_of_birth(
            '1989-3-1')

        assert dob_day == 1
        assert dob_month == 3
        assert dob_year == 1989

        dob_day, dob_month, dob_year = parse_date_of_birth(
            '1913-1-13')

        assert dob_day == 13
        assert dob_month == 1
        assert dob_year == 1913

    def test_day_first_with_dot_separators(self):
        test_date = '11.10.1989'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date)

        assert dob_day == 11
        assert dob_month == 10
        assert dob_year == 1989

    def test_day_first_with_space_separators(self):
        test_date = '11 10 1989'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date)

        assert dob_day == 11
        assert dob_month == 10
        assert dob_year == 1989

    def test_day_first_with_separators(self):
        test_date = '1989-11-10'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date)

        assert dob_day == 10
        assert dob_month == 11
        assert dob_year == 1989

    def test_has_time(self):
        test_date = '1950-02-27 00:00:00'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date)

        assert dob_day == 27
        assert dob_month == 2
        assert dob_year == 1950

    def test_day_less_than_13(self):
        test_date = '2021-06-08 00:00:00'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date)

        assert dob_day == 8
        assert dob_month == 6
        assert dob_year == 2021

    def test_empty_string(self):
        test_date = ''
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date)

        assert dob_day == ''
        assert dob_month == ''
        assert dob_year == ''

    def test_undefined(self):
        test_date = None
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date)

        assert dob_day == ''
        assert dob_month == ''
        assert dob_year == ''

    def test_short_year_year_first(self):
        test_date = '20020520'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date)

        assert dob_day == 20
        assert dob_month == 5
        assert dob_year == 2002


class TestCaseNoteNeedsAnUpdate:
    def setup_method(self):
        self.fake = Faker()

    def test_case_notes_does_not_need_an_update(self):
        new_note = self.fake.sentence()

        case_notes_on_request = [{'author': self.fake.name(),
                                  'noteDate': self.fake.date(),
                                  'note': "Giant Orc"},
                                 {'author': self.fake.name(),
                                  'noteDate': self.fake.date(),
                                  'note': new_note}]

        result = case_note_needs_an_update(case_notes_on_request, new_note)
        assert result == False

    def test_case_notes_need_an_update(self):
        case_notes_on_request = [{'author': self.fake.name(),
                                  'noteDate': self.fake.date(),
                                  'note': self.fake.sentence()}]

        new_note = self.fake.sentence()

        result = case_note_needs_an_update(case_notes_on_request, new_note)
        assert result

    def test_case_notes_need_an_update_two(self):
        case_notes_on_request = [
            {'author': self.fake.name(),
             'noteDate': self.fake.date(),
             'note': self.fake.sentence()},
            {'author': self.fake.name(),
             'noteDate': self.fake.date(),
             'note': self.fake.sentence()}
        ]

        new_note = self.fake.sentence()

        result = case_note_needs_an_update(case_notes_on_request, new_note)
        assert result

    def test_case_notes_need_an_update_empty(self):
        case_notes_on_request = []
        new_note = self.fake.sentence()

        result = case_note_needs_an_update(case_notes_on_request, new_note)
        assert result


class TestCaseResidentIsIdentifiable:
    def setup_method(self):
        self.fake = Faker()

    def test_has_nhs_number_returns_true(self):
        assert resident_is_identifiable(help_request={
            "FirstName": 'Mr',
            "LastName": 'Zebra',
            "DobDay": 12,
            "DobMonth": 1,
            "DobYear": 1985,
            "ContactTelephoneNumber": "01234",
            "ContactMobileNumber": "344",
            "NhsNumber": "1231233",
            "NhsCtasId": ""
        })

    def test_name_and_nhs_number_missing_returns_false(self):
        assert resident_is_identifiable(help_request={
            "FirstName": '',
            "LastName": 'Zebra',
            "DobDay": 12,
            "DobMonth": 1,
            "DobYear": 1985,
            "ContactTelephoneNumber": "01234",
            "ContactMobileNumber": "344",
            "NhsNumber": "",
            "NhsCtasId": ""
        }) == False

    def test_name_combined_with_other_key_fields_match_if_nhs_number_is_missing(self):
        assert resident_is_identifiable(help_request={
            "FirstName": 'Mr',
            "LastName": 'Zebra'
        }) == False

        assert resident_is_identifiable(help_request={
            "FirstName": 'Mr',
            "LastName": 'Zebra',
            "DobDay": 12,
            "DobMonth": 1,
            "DobYear": 1985,
        })

        assert resident_is_identifiable(help_request={
            "FirstName": 'Mr',
            "LastName": 'Zebra',
            "NhsCtasId": '1',
        })

        assert resident_is_identifiable(help_request={
            "FirstName": 'Mr',
            "LastName": 'Zebra',
            "NhsCtasId": '1',
        })

        assert resident_is_identifiable(help_request={
            "FirstName": 'Mr',
            "LastName": 'Zebra',
            "ContactTelephoneNumber": '13434',
        })

        assert resident_is_identifiable(help_request={
            "FirstName": 'Mr',
            "LastName": 'Zebra',
            "ContactMobileNumber": '13434',
        })

        assert resident_is_identifiable(help_request={
            "FirstName": 'Mr',
            "LastName": 'Zebra',
            "EmailAddress": 'mr@zebra.safari',
        })

class TestManualParseMethodForDates:
    def test_dmYHM_slash_date_returns_valid_date(self):
        # arrange
        test_date_1 = '09/11/2021 00:00'
        expected_1 = datetime.datetime(2021,11,9,0,0)
        
        test_date_2 = '07/01/2021 18:57'
        expected_2 = datetime.datetime(2021,1,7,18,57)

        # act
        parsed_date_str_1 = manual_parse(test_date_1)
        parsed_date_str_2 = manual_parse(test_date_2)

        # assert
        assert (parsed_date_str_1 - expected_1).total_seconds() == 0
        assert (parsed_date_str_2 - expected_2).total_seconds() == 0
    
    def test_dmY_slash_date_returns_valid_date(self):
        # arrange
        test_date_1 = '24/05/2022'
        expected_1 = datetime.datetime(2022,5,24)
        
        test_date_2 = '18/03/2020'
        expected_2 = datetime.datetime(2020,3,18)

        # act
        parsed_date_str_1 = manual_parse(test_date_1)
        parsed_date_str_2 = manual_parse(test_date_2)

        # assert
        assert (parsed_date_str_1 - expected_1).total_seconds() == 0
        assert (parsed_date_str_2 - expected_2).total_seconds() == 0
    
    def test_dmYHMS_slash_date_returns_valid_date(self):
        # arrange
        test_date_1 = '15/01/2022 00:00:00'
        expected_1 = datetime.datetime(2022,1,15,0,0,0)
        
        test_date_2 = '25/12/2021 07:22:45'
        expected_2 = datetime.datetime(2021,12,25,7,22,45)

        # act
        parsed_date_str_1 = manual_parse(test_date_1)
        parsed_date_str_2 = manual_parse(test_date_2)

        # assert
        assert (parsed_date_str_1 - expected_1).total_seconds() == 0
        assert (parsed_date_str_2 - expected_2).total_seconds() == 0
