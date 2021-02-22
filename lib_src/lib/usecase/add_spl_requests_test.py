from .add_spl_requests import AddSPLRequests
import pandas as pd
from .fakes.fake_create_help_request import FakeCreateHelpRequest
import datetime


def test_a_new_help_request_is_added():
    create_Help_request = FakeCreateHelpRequest()

    data_frame = pd.DataFrame({
        'Traced_NHSNUMBER': ['2649260211', '1234567890'],
        'PatientFirstName': ['Homer', 'Shaco'],
        'PatientOtherName': ['Jay', ''],
        'PatientSurname': ['Simpson', 'N00b'],
        'DateOfBirth': ['19560512', '19930329'],
        'PatientAddress_Line1': ['742 Evergreen Terrace', '404 Summoner rf'],
        'PatientAddress_Line2': ['', ''],
        'PatientAddress_Line3': ['Springfield', 'Black Hole'],
        'PatientAddress_Line4': ['', ''],
        'PatientAddress_Line5': ['', ''],
        'PatientAddress_PostCode': ['TS1 2SP', 'CH5 5AP'],
        'PatientEmailAddress': ['homer@email.com', 'n00b4lyfe@mail.com'],
        'mobile': ['0723083534', '07123456789'],
        'landline': ['0278460422', '021234567890'],
        'DateOfDeath': ['', '21-02-2021'],
        'Flag_PDSInformallyDeceased': ['0', '0'],
        'oslaua': ['E09000012', ''],
        'oscty': ['E99999999', ''],
        'Data_Source': ['COVID-19 PRA', 'Initial'],
        'category': ['Added by COVID-19 Population Risk Assessment', 'Deceased'],
        'InceptionDate': ['44242', '2020-04-22'],
        'SPL_Version': ['44', ''],
        'uprn': ['10008326160', '02938372719']
    })

    use_case = AddSPLRequests(create_Help_request)
    processed_data_frame = use_case.execute(data_frame=data_frame)

    assert len(create_Help_request.received_help_requests) == 2

    case_note = "SPL Category: Added by COVID-19 Population Risk Assessment."

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

    assert create_Help_request.received_help_requests[1] == {
        'Metadata': {
            'spl_id': '1234567890'},
        'Uprn': '02938372719',
        'Postcode': 'CH5 5AP',
        'AddressFirstLine': '404 Summoner rf',
        'AddressSecondLine': '',
        'AddressThirdLine': 'Black Hole',
        'CaseNotes': f'{{"author":"Data Ingestion: Shielding Patient List","noteDate":" {note_date}","note":"SPL Category: Deceased. Date of death: 21-02-2021"}}',
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

    assert processed_data_frame.iloc[0].help_request_id == 123
