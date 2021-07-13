from lib_src.lib.usecase.add_self_isolation_requests import AddSelfIsolationRequests
import pandas as pd
from lib_src.tests.fakes.fake_create_help_request import FakeCreateHelpRequest
from lib_src.tests.fakes.fake_here_to_help_gateway import FakeHereToHelpGateway
import datetime


def get_data_frame(la_support_letter_received=['1', '', '1'],
                   la_support_required=['0', '1', '1'],
                   day_7_outcome=['', '', ''],
                   day_13_outcome=['', '', ''],
                   status_report=['completed', 'completed', 'completed'],
                   date_tested=[datetime.date.today().strftime("%d/%m/%Y"), datetime.date.today().strftime("%d/%m/%Y"),
                                datetime.date.today().strftime("%d/%m/%Y")]):
    return pd.DataFrame({
        'UPRN': ['A UPRN', 'A UPRN 2', 'A UPRN 3'],
        'Postcode': ['BS3 3NG', 'BS4', 'BS5'],
        'House Number': ['61', '62', '63'],
        'Address Line 1': ['A Road', 'A Road 2', 'A Road 3'],
        'Address Line 2': ['Somewhere', 'Somewhere 2', 'Somewhere 3'],
        'Town': ['Hereford', 'Shire', 'Earth'],
        'Date of Birth': ['', '', ''],
        'Forename': ['Owen', 'Someone', 'Another'],
        'Surname': ['Test', 'Surname', 'Lastname'],
        'Phone2': ['000', '0123', '34'],
        'Phone': ['000', '2314', '1234'],
        'Email': ['owen@test', 'test@someone.com', 'test2343@asite.com'],
        'Status Report': status_report,
        'NHS Number': ['123412345', '92342323', '24359e43'],
        'ID': ['123', '144', '555'],
        'LA Support Letter Received': la_support_letter_received,
        'LA Support Required': la_support_required,
        'Day 4 Outcome': ['', '', ''],
        'Day 7 Outcome': day_7_outcome,
        'Day 10 Outcome': ['', '', ''],
        'Day 13 Outcome': day_13_outcome,
        'Comments': ['', '', ''],
        "Date Tested": date_tested
    })


# CallbackRequired = either LA Support Letter Received or LA Support Required fields contain 1.
def test_only_callback_required_rows_processed():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121231
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id)

    data_frame = get_data_frame()

    use_case = AddSelfIsolationRequests(create_help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert (processed_data_frame.at[0, 'help_request_id'] is not None)

    assert create_help_request.received_help_requests[1]['Metadata'] == {
        "LA_support_required": '1',
        "LA_support_letter_received": ''
    }

    assert len(create_help_request.received_help_requests) == 3


def test_callback_not_required_rows_ignored():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121231
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id)

    data_frame = get_data_frame(la_support_letter_received=['0', '', '0'], la_support_required=['0', '', ''])

    use_case = AddSelfIsolationRequests(create_help_request, here_to_help_api)
    use_case.execute(data_frame=data_frame)

    assert len(create_help_request.received_help_requests) == 0


def test_la_support_letter_received_creates_cev_record():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121233
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id, cev_exists=False)

    data_frame = get_data_frame()

    use_case = AddSelfIsolationRequests(create_help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert (processed_data_frame.at[0, 'cev_case_added_id'] == 1)
    assert (processed_data_frame.at[1, 'cev_case_added_id'] == '')
    assert (processed_data_frame.at[2, 'cev_case_added_id'] == 1)

    assert len(here_to_help_api.get_multiple_help_requests_called_with) == 2
    assert len(here_to_help_api.create_resident_help_request_called_with) == 2

    assert here_to_help_api.create_case_note_called_with[1] == {
        'resident_id': 121233,
        'help_request_id': 1,
        'case_note': {
            "author": "Data Ingestion: Self Isolation",
            "note": "--- self-reported CEV resident identified through self-isolation support "
                    "process ---"}
    }


def test_la_support_letter_received_does_not_create_cev_record_if_one_exists():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121233
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id)

    data_frame = get_data_frame()

    use_case = AddSelfIsolationRequests(create_help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert (processed_data_frame.at[0, 'cev_case_added_id'] == '')
    assert (processed_data_frame.at[1, 'cev_case_added_id'] == '')
    assert (processed_data_frame.at[2, 'cev_case_added_id'] == '')

    assert len(here_to_help_api.get_multiple_help_requests_called_with) == 2
    assert len(here_to_help_api.create_resident_help_request_called_with) == 0


def test_day_outcome_columns_become_case_notes():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121231
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id, test_case_note="Day 13 Outcome: day13")

    data_frame = get_data_frame(la_support_letter_received=['0', '', '0'],
                                la_support_required=['1', '', ''],
                                day_7_outcome=['day7', '', ''],
                                day_13_outcome=['day13', '', ''])

    use_case = AddSelfIsolationRequests(create_help_request, here_to_help_api)

    use_case.execute(data_frame)

    assert len(here_to_help_api.create_case_note_called_with) == 1

    assert here_to_help_api.create_case_note_called_with[0] == {
        'resident_id': 121231,
        'help_request_id': 1,
        'case_note': {
            "author": "Data Ingestion: Self Isolation",
            "note": "Day 7 Outcome: day7"}
    }


# most of this might be irrelevant - no time to examine
def test_rows_only_get_processed_when_status_report_is_completed():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 125551
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id)

    data_frame = get_data_frame(
        la_support_letter_received=['1', '1', '1'],
        la_support_required=['1', '1', '1'],
        status_report=['completed', 'failed', 'completed'])

    use_case = AddSelfIsolationRequests(create_help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    # check whether the correct help request got imported
    assert any(
        help_request.get("NhsNumber") == "123412345" for help_request in create_help_request.received_help_requests)
    assert any(
        help_request.get("NhsNumber") == "24359e43" for help_request in create_help_request.received_help_requests)

    # check whether the correct quantity of help request has gotten imported
    assert len(create_help_request.received_help_requests) == 2


def test_only_rows_newer_than_seven_days_get_processed():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121231
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id)

    la_support_letter_received = ['', '', '']
    la_support_required = ['1', '1', '1']

    invalid_date = datetime.date.today() - datetime.timedelta(days=80)
    invalid_edge_date = datetime.date.today() - datetime.timedelta(days=7)
    valid_edge_date = datetime.date.today() - datetime.timedelta(days=6)

    data_frame = get_data_frame(la_support_letter_received=la_support_letter_received,
                                la_support_required=la_support_required,
                                date_tested=[invalid_date.strftime("%d/%m/%Y %H:%M:%S"),
                                             invalid_edge_date.strftime("%d/%m/%Y"),
                                             valid_edge_date.strftime("%d-%m-%Y")])

    use_case = AddSelfIsolationRequests(create_help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert (processed_data_frame.at[0, 'help_request_id'] is not None)

    assert len(create_help_request.received_help_requests) == 1

def test_ignore_rows_with_no_date_tested_processed():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121231
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id)

    la_support_letter_received = ['', '', '']
    la_support_required = ['1', '1', '1']

    valid_date = datetime.date.today()

    data_frame = get_data_frame(la_support_letter_received=la_support_letter_received,
                                la_support_required=la_support_required,
                                date_tested=[valid_date.strftime("%d/%m/%Y"),
                                             '',
                                             ''])

    use_case = AddSelfIsolationRequests(create_help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert (processed_data_frame.at[0, 'help_request_id'] is not None)

    assert len(create_help_request.received_help_requests) == 1
