import datetime as dt
from .process_contact_tracing_calls import ProcessContactTracingCalls
from .fakes.fake_google_drive_gateway import FakeGoogleDriveGateway
from .fakes.fake_pygsheet_gateway import FakePygsheetGateway
from .fakes.fake_add_contact_tracing_requests import FakeAddContactTracingRequests

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
POWER_BI = {
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
            'Date Tested': ['09/12/2020'],
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
        }

def test_processing_new_power_bi_spreadsheet():
    fake_google_drive_gateway = FakeGoogleDriveGateway(True, False)
    fake_pygsheet_gateway = FakePygsheetGateway(POWER_BI)
    fake_add_contact_tracing_requests = FakeAddContactTracingRequests()

    use_case = ProcessContactTracingCalls(fake_google_drive_gateway,fake_pygsheet_gateway,fake_add_contact_tracing_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id')

    today = dt.datetime.now().date().strftime('%Y-%m-%d')

    assert len(fake_google_drive_gateway.search_folder_calls) == 2

    assert len(fake_google_drive_gateway.created_spreadsheets) == 2

    assert fake_google_drive_gateway.created_spreadsheets == [
        {'folder_id': 'outbound_folder_id', 'spreadsheet_name': 'Hackney_CT_FOR_UPLOAD_'+today},
        {'folder_id': 'outbound_folder_id', 'spreadsheet_name': 'city_CT_FOR_UPLOAD_'+today}
    ]

    assert fake_pygsheet_gateway.get_data_frame_from_sheet_called_with == [['inbound_folder_id', 'A3']]

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 2

    assert len(fake_add_contact_tracing_requests.execute_called_with) == 1

def test_new_power_bi_spreadsheet_but_it_has_been_processed():
    fake_google_drive_gateway = FakeGoogleDriveGateway(True, True)
    fake_pygsheet_gateway = FakePygsheetGateway(POWER_BI)
    fake_add_contact_tracing_requests = FakeAddContactTracingRequests()

    use_case = ProcessContactTracingCalls(fake_google_drive_gateway,fake_pygsheet_gateway,fake_add_contact_tracing_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id')

    assert len(fake_google_drive_gateway.search_folder_calls) == 2

    assert len(fake_google_drive_gateway.created_spreadsheets) == 0

    assert len(fake_pygsheet_gateway.get_data_frame_from_sheet_called_with) == 0

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 0

    assert len(fake_add_contact_tracing_requests.execute_called_with) == 0

def test_no_new_power_bi_spreadsheet_to_process():
    fake_google_drive_gateway = FakeGoogleDriveGateway(False, False)
    fake_pygsheet_gateway = FakePygsheetGateway(POWER_BI)
    fake_add_contact_tracing_requests = FakeAddContactTracingRequests()

    use_case = ProcessContactTracingCalls(fake_google_drive_gateway,fake_pygsheet_gateway,fake_add_contact_tracing_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id')

    assert len(fake_google_drive_gateway.search_folder_calls) == 1

    assert len(fake_google_drive_gateway.created_spreadsheets) == 0

    assert len(fake_pygsheet_gateway.get_data_frame_from_sheet_called_with) == 0

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 0

    assert len(fake_add_contact_tracing_requests.execute_called_with) == 0
