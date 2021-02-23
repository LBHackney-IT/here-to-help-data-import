import datetime as dt
from lib_src.lib.usecase.process_spl_calls import ProcessSPLCalls
from lib_src.tests.fakes.fake_google_drive_gateway import FakeGoogleDriveGateway
from lib_src.tests.fakes.fake_pygsheet_gateway import FakePygsheetGateway
from lib_src.tests.fakes.fake_add_cev_requests import FakeAddCEVRequests

SPL = {
    'Traced_NHSNUMBER': ['2649260211'],
    'PatientFirstName': ['Homer'],
    'PatientOtherName': ['Jay'],
    'PatientSurname': ['Simpson'],
    'DateOfBirth': ['19560512'],
    'PatientAddress_Line1': ['742 Evergreen Terrace'],
    'PatientAddress_Line2': [''],
    'PatientAddress_Line3': ['Springfield'],
    'PatientAddress_Line4': [''],
    'PatientAddress_Line5': [''],
    'PatientAddress_PostCode': ['TS1 2SP'],
    'PatientEmailAddress': ['homer@email.com'],
    'mobile': ['0723083534'],
    'landline': ['0278460422'],
    'DateOfDeath': [''],
    'Flag_PDSInformallyDeceased': ['0'],
    'oslaua': ['E09000012'],
    'oscty': ['E99999999'],
    'Data_Source': ['COVID-19 PRA'],
    'category': ['Added by COVID-19 Population Risk Assessment'],
    'InceptionDate': ['44242'],
    'SPL_Version': ['44'],
    'uprn': ['10008326160'],
}


def test_processing_new_spl_spreadsheet():
    fake_google_drive_gateway = FakeGoogleDriveGateway(True, False)
    fake_pygsheet_gateway = FakePygsheetGateway(SPL)
    fake_add_cev_requests = FakeAddCEVRequests()

    use_case = ProcessSPLCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_cev_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id')

    today = dt.datetime.now().date().strftime('%Y-%m-%d')

    assert len(fake_google_drive_gateway.search_folder_calls) == 2

    assert len(fake_google_drive_gateway.created_spreadsheets) == 1

    assert fake_google_drive_gateway.created_spreadsheets == [
        {'folder_id': 'outbound_folder_id', 'spreadsheet_name': 'Hackney_SPL_CASES_' + today}
    ]

    assert fake_pygsheet_gateway.get_data_frame_from_sheet_called_with == [
        ['inbound_folder_id', 'A1']]

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 1

    assert len(fake_add_cev_requests.execute_called_with) == 1


def test_new_spl_spreadsheet_but_it_has_been_processed():
    fake_google_drive_gateway = FakeGoogleDriveGateway(True, True)
    fake_pygsheet_gateway = FakePygsheetGateway(SPL)
    fake_add_cev_requests = FakeAddCEVRequests()

    use_case = ProcessSPLCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_cev_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id')

    assert len(fake_google_drive_gateway.search_folder_calls) == 2

    assert len(fake_google_drive_gateway.created_spreadsheets) == 0

    assert len(fake_pygsheet_gateway.get_data_frame_from_sheet_called_with) == 0

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 0

    assert len(fake_add_cev_requests.execute_called_with) == 0


def test_no_new_spl_spreadsheet_to_process():
    fake_google_drive_gateway = FakeGoogleDriveGateway(False, False)
    fake_pygsheet_gateway = FakePygsheetGateway(SPL)
    fake_add_cev_requests = FakeAddCEVRequests()

    use_case = ProcessSPLCalls(
        fake_google_drive_gateway,
        fake_pygsheet_gateway,
        fake_add_cev_requests)

    use_case.execute('inbound_folder_id', 'outbound_folder_id')

    assert len(fake_google_drive_gateway.search_folder_calls) == 1

    assert len(fake_google_drive_gateway.created_spreadsheets) == 0

    assert len(fake_pygsheet_gateway.get_data_frame_from_sheet_called_with) == 0

    assert len(fake_pygsheet_gateway.populate_spreadsheet_called_with) == 0

    assert len(fake_add_cev_requests.execute_called_with) == 0
