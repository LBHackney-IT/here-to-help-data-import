import datetime as dt
import pandas as pd
from lib_src.lib.usecase.process_contact_tracing_calls import ProcessContactTracingCalls
from lib_src.tests.fakes.fake_google_drive_gateway import FakeGoogleDriveGateway
from lib_src.tests.fakes.fake_pygsheet_gateway import FakePygsheetGateway
from lib_src.tests.fakes.fake_add_contact_tracing_requests import FakeAddContactTracingRequests

# ['Category', 'ID', 'Account ID', 'CDR Specimen Request sk', 'Exposer ID',
#  'Exposure Group', 'Matched Person ID', 'Matched Exposer ID',
#  'Date Created', 'NHS Number', 'Forename', 'Surname', 'Gender',
#  'Date of Birth', 'Ethnicity', 'House Number', 'Postcode',
#  'Postcode Area ID', 'Email', 'Phone', 'Phone2', 'UTLA', 'UTLA Index',
#  'UTLA from Index', 'LTLA', 'LTLA Index', 'LTLA from Index',
#  'PHE Centre', 'PHE Centre Index', 'First Symptomatic At', 'Date Tested',
#  'Number of Contacts', 'Number of Occupations', 'Occupation',
#  'Occupation Type', 'Job Title', 'Job Postcode', 'Job Description',
#  'Activity Details', 'Care Home', 'Residence Type', 'HPT Code', 'Status',
#  'Status Report', 'Initial Tier', 'Final Tier', 'Call Centre Outcome',
#  'LA Support Required', 'LA Support Received',
#  'LA Support Letter Received', 'LA Support Filter', 'Comments',
#  'Day 4 Outcome', 'Day 7 Outcome', 'Day 10 Outcome', 'Day 13 Outcome',
#  'Isolation Follow Up', 'Isolation Start Date',
#  'Combined Date Completed', 'Delay Creation Completion Days',
#  'Date Failed Uncontactable', 'Date Updated', 'Date Time Extracted']
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
    'Date Created': ['10/12/2020'],
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


def test_processing_new_power_bi_spreadsheet():
    return_inbound_files = [
        {'name': "fake_inbound1.xlsx", 'id': '1'},
        {'name': "fake_inbound2.xlsx", 'id': '2'}
    ]
    return_outbound_files = [
        {'name': f'PROCESSED_1',
         'id': '1'},
        {'name': f'PROCESSED_2',
         'id': '2'},
    ]

    today = dt.datetime.now().date().strftime('%Y-%m-%d')
    fake_google_drive_gateway = FakeGoogleDriveGateway(True, True, return_inbound_files, return_outbound_files)
    fake_pygsheet_gateway = FakePygsheetGateway(get_data_frame(today))
    fake_add_contact_tracing_requests = FakeAddContactTracingRequests()

    use_case = ProcessContactTracingCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_contact_tracing_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id', [])

    assert len(fake_google_drive_gateway.get_list_of_files_called_with) == 2

    assert len(fake_google_drive_gateway.created_spreadsheets) == 2

    assert fake_google_drive_gateway.created_spreadsheets == [
        {'folder_id': 'outbound_folder_id', 'spreadsheet_name': 'Hackney_CT_FOR_UPLOAD_' + today},
        {'folder_id': 'outbound_folder_id', 'spreadsheet_name': 'city_CT_FOR_UPLOAD_' + today}
    ]

    assert fake_pygsheet_gateway.get_data_frame_from_sheet_called_with == [
        ['inbound_folder_id', 'A3']]

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 2

    assert len(fake_add_contact_tracing_requests.execute_called_with) == 1


def test_new_power_bi_spreadsheet_but_it_has_been_processed():
    return_inbound_files = [
        {'name': "fake_inbound1.xlsx", 'id': '1'}
    ]
    return_outbound_files = [
        {'name': f'PROCESSED_1',
         'id': '1'},
        {'name': f'PROCESSED_2',
         'id': '2'},
    ]

    fake_google_drive_gateway = FakeGoogleDriveGateway(True, True, return_inbound_files, return_outbound_files)
    fake_pygsheet_gateway = FakePygsheetGateway(get_data_frame(dt.datetime.now().date().strftime('%Y-%m-%d')))
    fake_add_contact_tracing_requests = FakeAddContactTracingRequests()

    use_case = ProcessContactTracingCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_contact_tracing_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id', [])

    assert len(fake_google_drive_gateway.get_list_of_files_called_with) == 2

    assert len(fake_google_drive_gateway.created_spreadsheets) == 0

    assert len(fake_pygsheet_gateway.get_data_frame_from_sheet_called_with) == 0

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 0

    assert len(fake_add_contact_tracing_requests.execute_called_with) == 0


def test_no_new_power_bi_spreadsheet_to_process():
    fake_google_drive_gateway = FakeGoogleDriveGateway(False, False)
    fake_pygsheet_gateway = FakePygsheetGateway(get_data_frame(dt.datetime.now().date().strftime('%Y-%m-%d')))
    fake_add_contact_tracing_requests = FakeAddContactTracingRequests()

    use_case = ProcessContactTracingCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_contact_tracing_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id', [])

    assert len(fake_google_drive_gateway.created_spreadsheets) == 0

    assert len(fake_pygsheet_gateway.get_data_frame_from_sheet_called_with) == 0

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 0

    assert len(fake_add_contact_tracing_requests.execute_called_with) == 0

def test_total_rows_exceeds_3000_does_not_process():
    fake_google_drive_gateway = FakeGoogleDriveGateway(True, False)

    data_frame = pd.DataFrame(get_data_frame(dt.datetime.now().date().strftime('%Y-%m-%d')))
    data_frame = data_frame.loc[data_frame.index.repeat(3001)]

    fake_pygsheet_gateway = FakePygsheetGateway(data_frame)
    fake_add_contact_tracing_requests = FakeAddContactTracingRequests()

    use_case = ProcessContactTracingCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_contact_tracing_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id', [])

    assert len(fake_add_contact_tracing_requests.execute_called_with) == 0

def test_rows_older_than_14_days_ago_dont_get_processed():
    fake_google_drive_gateway = FakeGoogleDriveGateway(True, False)

    invalid_date = dt.date.today() - dt.timedelta(days=80)
    invalid_edge_date = dt.date.today() - dt.timedelta(days=14)
    valid_edge_date = dt.date.today() - dt.timedelta(days=13)

    data_frame = get_data_frame(invalid_date.strftime('%d/%m/%Y'))

    fake_pygsheet_gateway = FakePygsheetGateway(data_frame)
    fake_add_contact_tracing_requests = FakeAddContactTracingRequests()

    use_case = ProcessContactTracingCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_contact_tracing_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id', [])

    assert len(fake_add_contact_tracing_requests.execute_called_with[0]) == 0

def test_excludes_excluded_ctas_ids():
    fake_google_drive_gateway = FakeGoogleDriveGateway(True, False)

    valid_edge_date = dt.date.today() - dt.timedelta(days=13)

    data_frame = get_data_frame(valid_edge_date.strftime('%d/%m/%Y'))

    fake_pygsheet_gateway = FakePygsheetGateway(data_frame)
    fake_add_contact_tracing_requests = FakeAddContactTracingRequests()

    use_case = ProcessContactTracingCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_contact_tracing_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id', ['dd034b2100'])

    assert len(fake_add_contact_tracing_requests.execute_called_with[0]) == 0
