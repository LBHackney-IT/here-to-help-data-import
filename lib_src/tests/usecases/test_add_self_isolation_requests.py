from lib_src.lib.usecase.add_self_isolation_requests import AddSelfIsolationRequests
import pandas as pd
from lib_src.tests.fakes.fake_create_help_request import FakeCreateHelpRequest
from lib_src.tests.fakes.fake_here_to_help_gateway import FakeHereToHelpGateway


# CallbackRequired = either LA Support Letter Received or LA Support Required fields contain 1.
def test_only_callback_required_rows_processed():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121231
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id)

    data_frame = pd.DataFrame({
        'UPRN': ['A UPRN', 'A UPRN 2', 'A UPRN 3'],
        'Postcode': ['BS3 3NG', 'BS4', 'BS5'],
        'House Number': ['61','62', '63'],
        'Address Line 1': ['A Road', 'A Road 2', 'A Road 3'],
        'Address Line 2': ['Somewhere', 'Somewhere 2', 'Somewhere 3'],
        'Town': ['Hereford', 'Shire', 'Earth'],
        'Date of Birth': ['', '', ''],
        'Forename': ['Owen', 'Someone', 'Another'],
        'Surname': ['Test', 'Surname','Lastname'],
        'Phone2': ['000', '0123','34'],
        'Phone': ['000','2314','1234'],
        'Email': ['owen@test', 'test@someone.com','test2343@asite.com'],
        'NHS Number': ['123412345', '92342323','24359e43'],
        'ID': ['123','144','555'],
        'LA Support Letter Received': ['1', '', '1'],
        'LA Support Required': ['0','1','1']
    })

    use_case = AddSelfIsolationRequests(create_help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert len(create_help_request.received_help_requests) == 3

def test_callback_not_required_rows_ignored():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121231
    here_to_help_api = FakeHereToHelpGateway(test_resident_id=test_resident_id)

    data_frame = pd.DataFrame({
        'UPRN': ['A UPRN', 'A UPRN 2', 'A UPRN 3'],
        'Postcode': ['BS3 3NG', 'BS4', 'BS5'],
        'House Number': ['61','62', '63'],
        'Address Line 1': ['A Road', 'A Road 2', 'A Road 3'],
        'Address Line 2': ['Somewhere', 'Somewhere 2', 'Somewhere 3'],
        'Town': ['Hereford', 'Shire', 'Earth'],
        'Date of Birth': ['', '', ''],
        'Forename': ['Owen', 'Someone', 'Another'],
        'Surname': ['Test', 'Surname','Lastname'],
        'Phone2': ['000', '0123','34'],
        'Phone': ['000','2314','1234'],
        'Email': ['owen@test', 'test@someone.com','test2343@asite.com'],
        'NHS Number': ['123412345', '92342323','24359e43'],
        'ID': ['123','144','555'],
        'LA Support Letter Received': ['0', '', '0'],
        'LA Support Required': ['0','','']
    })

    use_case = AddSelfIsolationRequests(create_help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert len(create_help_request.received_help_requests) == 0
