from ..helpers import clean_data


class ProcessGenericIngestionCalls:
    COLS = [
        'First name',
        'Surname',
        'd.o.b',
        'Help Request Type',
        'Address Line 1',
        'Address Line 2',
        'City',
        'Postcode',
        'Email',
        'Phone number',
        'Phone number 2',
        'UPRN',
        'Subtype',
        'Case Note 1',
        'Case Note 2',
        'Case Note 3',
        'Case Note 4'
    ]

    def __init__(self, add_generic_ingestion_requests):
        self.add_generic_ingestion_requests = add_generic_ingestion_requests

    def execute(self, data_frame):
        data_frame = clean_data(columns=self.COLS, data_frame=data_frame)

        processed_data_frame = self.add_generic_ingestion_requests.execute(data_frame)

        return processed_data_frame
