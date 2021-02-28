from lib_src.lib.usecase.process_spl_calls import ProcessSPLCalls
from lib_src.tests.fakes.fake_add_cev_requests import FakeAddCEVRequests
import pandas as pd

SPL = {
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
    'uprn': ['10008326160'],
}


def test_processing_new_spl_spreadsheet():
    fake_add_cev_requests = FakeAddCEVRequests()

    use_case = ProcessSPLCalls(fake_add_cev_requests)

    use_case.execute(pd.DataFrame(data=[SPL]))

    assert len(fake_add_cev_requests.execute_called_with) == 1
