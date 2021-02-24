import pytest
from faker import Faker
from lib_src.lib.helpers import parse_date_of_birth, case_note_needs_an_update


class TestParseDateOfBirth:

    def test_year_first_no_separators(self):
        test_date = '19830502'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date, year_first=True)

        assert dob_day == 2
        assert dob_month == 5
        assert dob_year == 1983

    def test_year_first_with_separators(self):
        test_date = '1983-05-02'
        dob_day, dob_month, dob_year = parse_date_of_birth(test_date)

        assert dob_day == 2
        assert dob_month == 5
        assert dob_year == 1983

    def test_day_first_with_separators(self):
        test_date = '11/10/1989'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date, day_first=True)

        assert dob_day == 11
        assert dob_month == 10
        assert dob_year == 1989

    def test_empty_string(self):
        test_date = ''
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date, day_first=True)

        assert dob_day == ''
        assert dob_month == ''
        assert dob_year == ''

    def test_undefined(self):
        test_date = None
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date, day_first=True)

        assert dob_day == ''
        assert dob_month == ''
        assert dob_year == ''

    def test_short_year(self):
        test_date = '200596'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date, day_first=True)

        assert dob_day == 20
        assert dob_month == 5
        assert dob_year == 1996

    def test_short_year_year_first(self):
        test_date = '020520'
        dob_day, dob_month, dob_year = parse_date_of_birth(
            test_date, year_first=True)

        assert dob_day == 20
        assert dob_month == 5
        assert dob_year == 2002


class TestCaseNoteNeedsAnUpdate:
    def setup_method(self, method):
        self.fake = Faker(['en-GB', 'en_GB', 'en_GB', 'en-GB'])
        print(method)

    def test_case_notes_does_not_need_an_update(self):
        new_note = self.fake.sentence()

        case_notes_on_request = [{'author': self.fake.name(),
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
