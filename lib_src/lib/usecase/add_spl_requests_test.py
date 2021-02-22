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
