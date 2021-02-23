from lib_src.lib.usecase.add_spl_requests import AddSPLRequests
import pandas as pd
from lib_src.tests.fakes.fake_create_help_request import FakeCreateHelpRequest
from .fakes.fake_here_to_help_gateway import FakeHereToHelpGateway


def test_a_new_help_request_and_case_note_is_added():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 121231
    here_to_help_api = FakeHereToHelpGateway(test_resident_id)

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

    use_case = AddSPLRequests(create_help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert len(create_help_request.received_help_requests) == 1

    assert create_help_request.received_help_requests[0] == {
        'Uprn': '10008326160',
        'Metadata': {
            'spl_id': '2649260211'},
        'Postcode': 'TS1 2SP',
        'AddressFirstLine': '742 Evergreen Terrace',
        'AddressSecondLine': '',
        'AddressThirdLine': 'Springfield',
        # 'CaseNotes': f'{{"author":"Data Ingestion: Shielding Patient List","noteDate":" {note_date}","note":"{case_note}"}}',
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
    # assert create_help_request.received_help_requests[1] == {
    #     'Metadata': {
    #         'spl_id': '1234567890'},
    #     'Uprn': '02938372719',
    #     'Postcode': 'CH5 5AP',
    #     'AddressFirstLine': '404 Summoner rf',
    #     'AddressSecondLine': '',
    #     'AddressThirdLine': 'Black Hole',
    #     # 'CaseNotes': f'{{"author":"Data Ingestion: Shielding Patient List","noteDate":" {note_date}","note":"SPL Category: Deceased. Date of death: 21-02-2021"}}',
    #     'HelpWithSomethingElse': True,
    #     'FirstName': 'Shaco',
    #     'LastName': 'N00b',
    #     'DobDay': '29',
    #     'DobMonth': '3',
    #     'DobYear': '1993',
    #     'ContactTelephoneNumber': '021234567890',
    #     'ContactMobileNumber': '07123456789',
    #     'EmailAddress': 'n00b4lyfe@mail.com',
    #     'CallbackRequired': False,
    #     'HelpNeeded': 'Shielding',
    #     'NhsNumber': '1234567890'}

    test_help_request_id = create_help_request.get_returned_id()

    assert len(here_to_help_api.get_help_request_called_with) == 1

    assert here_to_help_api.get_help_request_called_with[0] == test_help_request_id

    assert len(here_to_help_api.create_case_note_called_with) == 1

    assert here_to_help_api.create_case_note_called_with[0] == {
        'case_note': {
            'author': 'Data Ingestion: Shielding Patient List',
            'note': 'SPL Category: Added by COVID-19 Population Risk Assessment.'},
        'help_request_id': test_help_request_id,
        'resident_id': 1162}

    # assert here_to_help_api.create_case_note_called_with[1] == {
    #     'case_note': {
    #         'author': 'Data Ingestion: Shielding Patient List',
    #         'note': 'SPL Category: Deceased. Date of death: 21-02-2021'
    #     },
    #     'help_request_id': 123,
    #     'resident_id': 1162
    # }
    assert processed_data_frame.iloc[0].help_request_id == test_help_request_id


def test_a_new_help_request_and_no_new_case_note_is_added():
    create_help_request = FakeCreateHelpRequest()

    test_resident_id = 312
    test_case_note = 'SPL Category: Deceased. Date of death: 21-02-2021'

    here_to_help_api = FakeHereToHelpGateway(
        test_resident_id, test_case_note=test_case_note)
    data_frame = pd.DataFrame({
        'Traced_NHSNUMBER': ['1234567890'],
        'PatientFirstName': ['Shaco'],
        'PatientOtherName': [''],
        'PatientSurname': ['N00b'],
        'DateOfBirth': ['19930329'],
        'PatientAddress_Line1': ['404 Summoner rf'],
        'PatientAddress_Line2': [''],
        'PatientAddress_Line3': ['Black Hole'],
        'PatientAddress_Line4': [''],
        'PatientAddress_Line5': [''],
        'PatientAddress_PostCode': ['CH5 5AP'],
        'PatientEmailAddress': ['n00b4lyfe@mail.com'],
        'mobile': ['07123456789'],
        'landline': ['021234567890'],
        'DateOfDeath': ['21-02-2021'],
        'Flag_PDSInformallyDeceased': ['0'],
        'oslaua': [''],
        'oscty': [''],
        'Data_Source': ['Initial'],
        'category': ['Deceased'],
        'InceptionDate': ['2020-04-22'],
        'SPL_Version': [''],
        'uprn': ['02938372719']

    })

    use_case = AddSPLRequests(create_help_request, here_to_help_api)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert len(create_help_request.received_help_requests) == 1

    assert create_help_request.received_help_requests[0] == {
        'Metadata': {
            'spl_id': '1234567890'},
        'Uprn': '02938372719',
        'Postcode': 'CH5 5AP',
        'AddressFirstLine': '404 Summoner rf',
        'AddressSecondLine': '',
        'AddressThirdLine': 'Black Hole',
        'HelpWithSomethingElse': True,
        'FirstName': 'Shaco',
        'LastName': 'N00b',
        'DobDay': '29',
        'DobMonth': '3',
        'DobYear': '1993',
        'ContactTelephoneNumber': '021234567890',
        'ContactMobileNumber': '07123456789',
        'EmailAddress': 'n00b4lyfe@mail.com',
        'CallbackRequired': False,
        'HelpNeeded': 'Shielding',
        'NhsNumber': '1234567890'}

    test_help_request_id = create_help_request.get_returned_id()

    assert len(here_to_help_api.get_help_request_called_with) == 1

    assert here_to_help_api.get_help_request_called_with[0] == test_help_request_id

    assert len(here_to_help_api.create_case_note_called_with) == 0

    assert processed_data_frame.iloc[0].help_request_id == test_help_request_id
