from add_cev_requests import AddCEVRequests
import pandas as pd
from fakes.fake_create_help_request import FakeCreateHelpRequest

NSSS = {
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
        'do_you_want_supermarket_deliveries': ['yes'],
        'do_you_need_someone_to_contact_you_about_local_support': ['yes']
    }

def test_create_help_request():
    create_Help_request = FakeCreateHelpRequest()

    data_frame = pd.DataFrame(NSSS)

    use_case = AddCEVRequests(create_Help_request)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert len(create_Help_request.received_help_requests) == 1

    assert create_Help_request.received_help_requests[0] == {
        'Uprn': '',
        'Postcode': 'BR2 9FF',
        'AddressFirstLine': '45 Cave Stone Road',
        'AddressSecondLine': '',
        'AddressThirdLine': 'Bedrock',
        'CaseNotes': 'Imported from National Shielding Service System list',
        'HelpWithAccessingSupermarketFood': True,
        'HelpWithSomethingElse': True,
        'FirstName': 'Fred',
        'LastName': 'Flintstone',
        'DobDay': '2',
        'DobMonth': '2',
        'DobYear': '1963',
        'ContactTelephoneNumber': '07344211233',
        'ContactMobileNumber': '02344211233',
        'EmailAddress': 'fred@rocks.st',
        'CallbackRequired': True,
        'HelpNeeded': 'Shielding',
        'NhsNumber': '1234567890'
    }

    assert processed_data_frame.iloc[0].help_request_id == 123
