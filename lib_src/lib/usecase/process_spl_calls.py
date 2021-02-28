from ..helpers import clean_data


class ProcessSPLCalls:
    COLS = [
        'Traced_NHSNUMBER',
        'PatientFirstName',
        'PatientOtherName',
        'PatientSurname',
        'DateOfBirth',
        'PatientAddress_Line1',
        'PatientAddress_Line2',
        'PatientAddress_Line3',
        'PatientAddress_Line4',
        'PatientAddress_Line5',
        'PatientAddress_PostCode',
        'PatientEmailAddress',
        'mobile',
        'landline',
        'DateOfDeath',
        'Flag_PDSInformallyDeceased',
        'oslaua',
        'oscty',
        'Data_Source',
        'category',
        'InceptionDate',
        'SPL_Version',
        'uprn'
    ]

    def __init__(self, add_spl_requests):
        self.add_spl_requests = add_spl_requests

    def execute(self, data_frame):
        data_frame = clean_data(columns=self.COLS, data_frame=data_frame)

        processed_data_frame = self.add_spl_requests.execute(data_frame)

        return processed_data_frame
