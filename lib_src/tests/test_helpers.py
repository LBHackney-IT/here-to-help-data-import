from lib_src.lib.helpers import parse_date_of_birth


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
