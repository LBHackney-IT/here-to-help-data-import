import datetime as dt
from process_cev_calls import ProcessCevCalls
from fakes.fake_google_drive_gateway import FakeGoogleDriveGateway
from fakes.fake_pygsheet_gateway import FakePygsheetGateway
from fakes.fake_add_cev_requests import FakeAddCEVRequests

NSSS = {
    'ID': ['123123'],
    'nhs_number': ['1234567890'],
    'first_name': ['Fred'],
    'last_name': ['Flintstone'],
    'date_of_birth': ['02/02/1963'],
    'address_line1': ['45 Cave Stone Road'],
    'address_line2': [''],
    'address_town_city': ['Bedrock'],
    'address_postcode': ['BR2 9FF'],
    'address_uprn': [''],
    'contact_number_calls': ['07344211233'],
    'contact_number_texts': ['02344211233'],
    'contact_email': ['fred@rocks.st'],
    'submission_datetime': ['27/01/2021 14:14:56'],
    'do_you_want_supermarket_deliveries': ['yes'],
    'do_you_need_someone_to_contact_you_about_local_support': ['yes']
}


# 'ID',
# 'middle_name',
# 'uid_submission',
# 'submission_datetime',
# 'are_you_applying_on_behalf_of_someone_else',
# 'have_you_received_an_nhs_letter',
# 'do_you_have_one_of_the_listed_medical_conditions',
# 'do_you_have_someone_to_go_shopping_for_you',
# 'ladcode',
# 'active_status',
# 'spl_category',
# 'spl_address_line1',
# 'spl_address_line2',
# 'spl_address_line3',
# 'spl_address_line4',
# 'spl_address_line5',
# 'spl_address_postcode',
# 'spl_address_uprn',
# 'help_request_id'

def test_processing_new_nsss_spreadsheet():
    fake_google_drive_gateway = FakeGoogleDriveGateway(True, False)
    fake_pygsheet_gateway = FakePygsheetGateway(NSSS)
    fake_add_cev_requests = FakeAddCEVRequests()

    use_case = ProcessCevCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_cev_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id')

    today = dt.datetime.now().date().strftime('%Y-%m-%d')

    assert len(fake_google_drive_gateway.search_folder_calls) == 2

    assert len(fake_google_drive_gateway.created_spreadsheets) == 1

    assert fake_google_drive_gateway.created_spreadsheets == [
        {'folder_id': 'outbound_folder_id', 'spreadsheet_name': 'Hackney_NSSS_CASES_' + today}
    ]

    assert fake_pygsheet_gateway.get_data_frame_from_sheet_called_with == [
        ['inbound_folder_id', 'A1']]

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 1

    assert len(fake_add_cev_requests.execute_called_with) == 1


def test_new_nsss_spreadsheet_but_it_has_been_processed():
    fake_google_drive_gateway = FakeGoogleDriveGateway(True, True)
    fake_pygsheet_gateway = FakePygsheetGateway(NSSS)
    fake_add_cev_requests = FakeAddCEVRequests()

    use_case = ProcessCevCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_cev_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id')

    assert len(fake_google_drive_gateway.search_folder_calls) == 2

    assert len(fake_google_drive_gateway.created_spreadsheets) == 0

    assert len(fake_pygsheet_gateway.get_data_frame_from_sheet_called_with) == 0

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 0

    assert len(fake_add_cev_requests.execute_called_with) == 0


def test_no_new_nsss_spreadsheet_to_process():
    fake_google_drive_gateway = FakeGoogleDriveGateway(False, False)
    fake_pygsheet_gateway = FakePygsheetGateway(NSSS)
    fake_add_cev_requests = FakeAddCEVRequests()

    use_case = ProcessCevCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_cev_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id')

    assert len(fake_google_drive_gateway.search_folder_calls) == 1

    assert len(fake_google_drive_gateway.created_spreadsheets) == 0

    assert len(fake_pygsheet_gateway.get_data_frame_from_sheet_called_with) == 0

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 0

    assert len(fake_add_cev_requests.execute_called_with) == 0
