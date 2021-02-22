from .add_spl_requests import AddSPLRequests
import pandas as pd
from .fakes.fake_create_help_request import FakeCreateHelpRequest
import datetime


def test_a_new_help_request_is_added():
    create_Help_request = FakeCreateHelpRequest()

    data_frame = pd.DataFrame({
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
        'uprn': ['10008326160']
    })

    use_case = AddSPLRequests(create_Help_request)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert len(create_Help_request.received_help_requests) == 1

    case_note = "SPL Category: Added by COVID-19 Population Risk Assessment"

    note_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")

    assert create_Help_request.received_help_requests[0] == {
        'Uprn': '10008326160',
        'Metadata': {
            'spl_id': '2649260211'},
        'Postcode': 'TS1 2SP',
        'AddressFirstLine': '742 Evergreen Terrace',
        'AddressSecondLine': '',
        'AddressThirdLine': 'Springfield',
        'CaseNotes': f'{{"author":"Data Ingestion: Shielding Patient List","noteDate":" {note_date}","note":"{case_note}"}}',
        'HelpWithSomethingElse': True,
        'FirstName': 'Homer',
        'LastName': 'Simpson',
        'DobDay': '12',
        'DobMonth': '5',
        'DobYear': '1956',
        'ContactTelephoneNumber': '0278460422',
        'ContactMobileNumber': '0723083534',
        'EmailAddress': 'homer@email.com',
        'CallbackRequired': False,
        'HelpNeeded': 'Shielding',
        'NhsNumber': '2649260211'}

    assert processed_data_frame.iloc[0].help_request_id == 123

# def test_case_note_is_added_when_answers_have_changed():
#     create_Help_request = FakeCreateHelpRequest()
#     here_to_help_api = FakeHereToHelpGateway()

#     data_frame = pd.DataFrame({
#         'ID': ['123123'],
#         'nhs_number': ['1234567890'],
#         'first_name': ['Fred'],
#         'last_name': ['Flintstone'],
#         'date_of_birth': ['02/02/1963'],
#         'address_line1': ['45 Cave Stone Road'],
#         'address_line2': [''],
#         'address_town_city': ['Bedrock'],
#         'address_postcode': ['BR2 9FF'],
#         'address_uprn': [''],
#         'contact_number_calls': ['07344211233'],
#         'contact_number_texts': ['02344211233'],
#         'contact_email': ['fred@rocks.st'],
#         'do_you_want_supermarket_deliveries': ['yes'],
#         'submission_datetime': ['27/01/2021 14:14:56'],
#         'do_you_need_someone_to_contact_you_about_local_support': ['yes'],
#         'do_you_have_someone_to_go_shopping_for_you': ['no']
#     })

#     use_case = AddSPLRequests(create_Help_request, here_to_help_api)
#     processed_data_frame = use_case.execute(data_frame=data_frame)

#     assert len(create_Help_request.received_help_requests) == 1

#     case_note = "CEV: Dec 2020 Tier 4 NSSS Submitted on:  27/01/2021 14:14:56. Do you want supermarket deliveries? " \
#                 "yes. Do you have someone to go shopping for you? no. Do you need someone to contact you about local " \
#                 "support? yes."

#     note_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")
#     assert create_Help_request.received_help_requests[0] == {
#         'Uprn': '',
#         'Metadata': {
#             'nsss_id': '123123'},
#         'Postcode': 'BR2 9FF',
#         'AddressFirstLine': '45 Cave Stone Road',
#         'AddressSecondLine': '',
#         'AddressThirdLine': 'Bedrock',
#         'CaseNotes': f'{{"author":"Data Ingestion: National Shielding Service System list","noteDate":" '
#         f'{note_date}","note":"{case_note}"}}',
#         'HelpWithSomethingElse': True,
#         'FirstName': 'Fred',
#         'LastName': 'Flintstone',
#         'DobDay': '2',
#         'DobMonth': '2',
#         'DobYear': '1963',
#         'ContactTelephoneNumber': '07344211233',
#         'ContactMobileNumber': '02344211233',
#         'EmailAddress': 'fred@rocks.st',
#         'CallbackRequired': True,
#         'HelpNeeded': 'Shielding',
#         'NhsNumber': '1234567890'}

#     assert processed_data_frame.iloc[0].help_request_id == 123

#     assert len(here_to_help_api.get_help_request_called_with) == 1

#     assert here_to_help_api.get_help_request_called_with[0] == 123

#     assert len(here_to_help_api.create_case_note_called_with) == 1

#     assert here_to_help_api.create_case_note_called_with[0] == {
#         'case_note': {
#             'author': 'Data Ingestion: National Shielding Service System '
#             'list',
#             'note': case_note,
#             'noteDate': note_date},
#         'help_request_id': 123,
#         'resident_id': 1162}
