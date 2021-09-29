from lib_src.lib.usecase.add_generic_ingestion_requests import AddGenericIngestionRequests
import pandas as pd
from lib_src.tests.fakes.fake_create_help_request import FakeCreateHelpRequest
from lib_src.tests.fakes.fake_here_to_help_gateway import FakeHereToHelpGateway
import datetime


def get_data_frame(help_request_type=['EUSS', 'unknown', 'EUSS'],
                   help_request_subtype=['', '', ''],
                   case_note_1=['', '', ''],
                   case_note_2=['', '', ''],
                   case_note_3=['', '', ''],
                   case_note_4=['', '', '']):
    return pd.DataFrame({
        'Postcode': ['BS3 3NG', 'BS4', 'BS5'],
        'Address Line 1': ['A Road', 'A Road 2', 'A Road 3'],
        'Address Line 2': ['Somewhere', 'Somewhere 2', 'Somewhere 3'],
        'City': ['Hereford', 'Shire', 'Earth'],
        'd.o.b': ['13/05/1985', '', ''],
        'First name': ['Owen', 'Someone', 'Another'],
        'Surname': ['Test', 'Surname', 'Lastname'],
        'Phone number': ['000', '0123', '34'],
        'Email': ['owen@test', 'notreal', ''],
        'Help Request Type': help_request_type,
        'Phone number 2': ['111', '', '89'],
        'UPRN': ['123', '', '909'],
        'Subtype': help_request_subtype,
        'Case Note 1': case_note_1,
        'Case Note 2': case_note_2,
        'Case Note 3': case_note_3,
        'Case Note 4': case_note_4,
    })


def test_only_known_help_request_type_rows_processed():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121231
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id)

    data_frame = get_data_frame()

    use_case = AddGenericIngestionRequests(create_help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert (processed_data_frame.at[0, 'help_request_id'] is not None)

    assert len(create_help_request.received_help_requests) == 2


def test_only_known_help_request_subtype_rows_processed():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121231
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id)

    data_frame = get_data_frame(help_request_type=['EUSS', 'Link Work', 'Link Work'],
                                help_request_subtype=['Repairs', '', 'Repairs'])

    use_case = AddGenericIngestionRequests(create_help_request, here_to_help_api)
    use_case.execute(data_frame=data_frame)

    assert len(create_help_request.received_help_requests) == 3


def test_day_outcome_columns_become_case_notes():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121231
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id)

    data_frame = get_data_frame(
        case_note_1=['1', '', ''],
        case_note_2=['case_note2', '', ''],
        case_note_3=['case_note3', '', ''],
        case_note_4=['case_note4', '', ''])

    use_case = AddGenericIngestionRequests(create_help_request, here_to_help_api)

    use_case.execute(data_frame=data_frame)

    assert len(here_to_help_api.create_case_note_called_with) == 4

    assert here_to_help_api.create_case_note_called_with[0] == {
        'resident_id': 121231,
        'help_request_id': 1,
        'case_note': {
            "author": "Data Ingestion: Generic Ingestion",
            "note": "Note from Data Ingestion: 1"}
    }
