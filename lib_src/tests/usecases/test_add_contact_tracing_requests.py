from lib_src.lib.usecase.add_contact_tracing_requests import AddContactTracingRequests
import pandas as pd
from lib_src.tests.fakes.fake_create_help_request import FakeCreateHelpRequest
import datetime

def get_data_frame(date_tested=None):
    return pd.DataFrame({
        'Category': ['case'],
        'ID': ['5270010'],
        'Account ID': ['dd034b2100'],
        'CDR Specimen Request sk': ['72893133'],
        'Exposer ID': [''],
        'Exposure Group': [''],
        'Matched Person ID': [5270310],
        'Matched Exposer ID': [''],
        'Date Created': ['10-12-2020'],
        'NHS Number': [1111122222],
        'Forename': ['Test'],
        'Surname': ['McTesty'],
        'Gender': ['male'],
        'Date of Birth': ['12/11/1998'],
        'Ethnicity': [''],
        'House Number': ['84'],
        'Postcode': ['e95hx'],
        'Postcode Area ID': [86],
        'Email': [''],
        'Phone': [''],
        'Phone2': [''],
        'UTLA': ['Hackney'],
        'UTLA Index': [''],
        'UTLA from Index': [False],
        'LTLA': ['Hackney'],
        'LTLA Index': [''],
        'LTLA from Index': [False],
        'PHE Centre': ['London'],
        'PHE Centre Index': [''],
        'First Symptomatic At': ['08/12/2020'],
        'Date Tested': [date_tested],
        'Number of Contacts': [2],
        'Number of Occupations': [4],
        'Occupation': ['Test'],
        'Occupation Type': ['Testing'],
        'Job Title': ['Test Dummy'],
        'Job Postcode': ['WC2H 9LL'],
        'Job Description': [''],
        'Activity Details': [''],
        'Care Home': [False],
        'Residence Type': [''],
        'HPT Code': ['hptnel'],
        'Status': ['local_follow_up'],
        'Status Report': ['failed'],
        'Initial Tier': ['Uncontactable'],
        'Final Tier': ['Tier 2'],
        'Call Centre Outcome': [''],
        'LA Support Required': [''],
        'LA Support Received': [''],
        'LA Support Letter Received': [''],
        'LA Support Filter': [''],
        'Comments': [''],
        'Day 4 Outcome': [''],
        'Day 7 Outcome': [''],
        'Day 10 Outcome': [''],
        'Day 13 Outcome': [''],
        'Isolation Follow Up': [''],
        'Isolation Start Date': ['07/12/2020'],
        'Combined Date Completed': [''],
        'Delay Creation Completion Days': [''],
        'Date Failed Uncontactable': [''],
        'Date Updated': ['10/12/2020'],
        'Date Time Extracted': ['1/21/21 3:53']
    })


def test_create_help_request():
    create_Help_request = FakeCreateHelpRequest()

    data_frame = get_data_frame(date_tested=datetime.date.today().strftime("%d/%m/%Y"))

    use_case = AddContactTracingRequests(create_Help_request)
    use_case.execute(data_frame=data_frame)

    assert len(create_Help_request.received_help_requests) == 1
    assert create_Help_request.received_help_requests[0]['Postcode'] == 'E95HX'
    assert create_Help_request.received_help_requests[0]['Postcode'] == 'E95HX'
    assert create_Help_request.received_help_requests[0]['AddressFirstLine'] == '84'
    assert create_Help_request.received_help_requests[0]['HelpWithSomethingElse']
    assert create_Help_request.received_help_requests[0]['FirstName'] == 'Test'
    assert create_Help_request.received_help_requests[0]['LastName'] == 'Mctesty'
    assert create_Help_request.received_help_requests[0]['DobDay'] == '12'
    assert create_Help_request.received_help_requests[0]['DobMonth'] == '11'
    assert create_Help_request.received_help_requests[0]['DobYear'] == '1998'
    assert create_Help_request.received_help_requests[0]['ContactTelephoneNumber'] == ''
    assert create_Help_request.received_help_requests[0]['ContactMobileNumber'] == ''
    assert create_Help_request.received_help_requests[0]['EmailAddress'] == ''
    assert create_Help_request.received_help_requests[0]['CallbackRequired']
    assert create_Help_request.received_help_requests[0]['CaseNotes'] == ''
    assert create_Help_request.received_help_requests[0]['HelpNeeded'] == 'Contact Tracing'
    assert create_Help_request.received_help_requests[0]['NhsNumber'] == 1111122222
    assert create_Help_request.received_help_requests[0]['NhsCtasId'] == 'dd034b2100'
    assert create_Help_request.received_help_requests[0]['Metadata'] == {
        'first_symptomatic_at': '08/12/2020', 'date_tested': datetime.date.today().strftime("%d/%m/%Y")
    }


def test_only_rows_newer_than_fourteen_days_get_processed():
    create_help_request = FakeCreateHelpRequest()

    invalid_date = datetime.date.today() - datetime.timedelta(days=80)
    invalid_edge_date = datetime.date.today() - datetime.timedelta(days=14)
    valid_edge_date = datetime.date.today() - datetime.timedelta(days=13)

    use_case = AddContactTracingRequests(create_help_request)

    processed_data_frame = use_case.execute(data_frame=get_data_frame(date_tested=invalid_date.strftime("%d/%m/%Y %H:%M:%S")))
    assert len(create_help_request.received_help_requests) == 0

    processed_data_frame = use_case.execute(
        data_frame=get_data_frame(date_tested=invalid_edge_date.strftime("%d/%m/%Y")))
    assert len(create_help_request.received_help_requests) == 0

    processed_data_frame = use_case.execute(
        data_frame=get_data_frame(date_tested=None))
    assert len(create_help_request.received_help_requests) == 0

    processed_data_frame = use_case.execute(
        data_frame=get_data_frame(date_tested=valid_edge_date.strftime("%d-%m-%Y")))
    assert len(create_help_request.received_help_requests) == 1

    assert create_help_request.received_help_requests[0]['Metadata'] == {
        'first_symptomatic_at': '08/12/2020', 'date_tested': valid_edge_date.strftime("%d-%m-%Y")
    }


