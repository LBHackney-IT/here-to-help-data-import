from lib_src.lib.usecase.add_generic_ingestion_requests import AddGenericIngestionRequests
import pandas as pd
from lib_src.tests.fakes.fake_create_help_request import FakeCreateHelpRequest
from lib_src.tests.fakes.fake_here_to_help_gateway import FakeHereToHelpGateway
import datetime


def get_data_frame(help_request_type=['EUSS', 'unknown', 'EUSS']):
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
        'Help Request Type': help_request_type
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