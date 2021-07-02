from ..helpers import clean_data


class ProcessSelfIsolationCalls:
    COLS = [
        'ID',
        'NHS Number',
        'Forename',
        'Surname',
        'Date of Birth',
        'House Number',
        'Address Line 1',
        'Address Line 2',
        'Town',
        'Postcode',
        'UPRN',
        'Email',
        'Phone',
        'Phone2',
        'LA Support Required',
        'LA Support Letter Received',
        'Day 4 Outcome',
        'Day 7 Outcome',
        'Day 10 Outcome',
        'Day 13 Outcome',
        'Comments'
    ]

    def __init__(self, add_self_isolation_requests):
        self.add_self_isolation_requests = add_self_isolation_requests

    def execute(self, data_frame):
        data_frame = clean_data(columns=self.COLS, data_frame=data_frame)

        processed_data_frame = self.add_self_isolation_requests.execute(data_frame)

        return processed_data_frame
