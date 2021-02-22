from lib_src.lib.usecase.add_cev_requests import AddCEVRequests
import pandas as pd
from .fakes.fake_create_help_request import FakeCreateHelpRequest
from .fakes.fake_here_to_help_gateway import FakeHereToHelpGateway
import datetime


def test_a_new_help_request_is_added():
    create_Help_request = FakeCreateHelpRequest()
    here_to_help_api = FakeHereToHelpGateway()

    data_frame = pd.DataFrame({
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
        'do_you_want_supermarket_deliveries': ['No'],
        'submission_datetime': ['2021-02-05T03:10:31Z'],
        'do_you_need_someone_to_contact_you_about_local_support': ['yes'],
        'do_you_have_someone_to_go_shopping_for_you': ['No']
    })

    use_case = AddCEVRequests(create_Help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert len(create_Help_request.received_help_requests) == 1

    case_note = "CEV: Dec 2020 Tier 4 NSSS Submitted on:  2021-02-05T03:10:31Z. Do you want supermarket deliveries? " \
                "No. Do you have someone to go shopping for you? No. Do you need someone to contact you about local " \
                "support? yes."

    note_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")

    assert create_Help_request.received_help_requests[0] == {
        'Uprn': '',
        'Metadata': {
            'nsss_id': '123123'},
        'Postcode': 'BR2 9FF',
        'AddressFirstLine': '45 Cave Stone Road',
        'AddressSecondLine': '',
        'AddressThirdLine': 'Bedrock',
        'CaseNotes': f'{{"author":"Data Ingestion: National Shielding Service System list","noteDate":" '
        f'{note_date}","note":"{case_note}"}}',
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
        'NhsNumber': '1234567890'}

    assert processed_data_frame.iloc[0].help_request_id == 123

    assert len(here_to_help_api.get_help_request_called_with) == 1

    assert here_to_help_api.get_help_request_called_with[0] == 123

    assert len(here_to_help_api.create_case_note_called_with) == 0


def test_case_note_is_added_when_answers_have_changed():
    create_Help_request = FakeCreateHelpRequest()
    here_to_help_api = FakeHereToHelpGateway()

    data_frame = pd.DataFrame({
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
        'do_you_want_supermarket_deliveries': ['yes'],
        'submission_datetime': ['27/01/2021 14:14:56'],
        'do_you_need_someone_to_contact_you_about_local_support': ['yes'],
        'do_you_have_someone_to_go_shopping_for_you': ['no']
    })

    use_case = AddCEVRequests(create_Help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert len(create_Help_request.received_help_requests) == 1

    case_note = "CEV: Dec 2020 Tier 4 NSSS Submitted on:  27/01/2021 14:14:56. Do you want supermarket deliveries? " \
                "yes. Do you have someone to go shopping for you? no. Do you need someone to contact you about local " \
                "support? yes."

    note_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")
    assert create_Help_request.received_help_requests[0] == {
        'Uprn': '',
        'Metadata': {
            'nsss_id': '123123'},
        'Postcode': 'BR2 9FF',
        'AddressFirstLine': '45 Cave Stone Road',
        'AddressSecondLine': '',
        'AddressThirdLine': 'Bedrock',
        'CaseNotes': f'{{"author":"Data Ingestion: National Shielding Service System list","noteDate":" '
        f'{note_date}","note":"{case_note}"}}',
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
        'NhsNumber': '1234567890'}

    assert processed_data_frame.iloc[0].help_request_id == 123

    assert len(here_to_help_api.get_help_request_called_with) == 1

    assert here_to_help_api.get_help_request_called_with[0] == 123

    assert len(here_to_help_api.create_case_note_called_with) == 1

    assert here_to_help_api.create_case_note_called_with[0] == {
        'case_note': {
            'author': 'Data Ingestion: National Shielding Service System '
            'list',
            'note': case_note,
            'noteDate': note_date},
        'help_request_id': 123,
        'resident_id': 1162}
