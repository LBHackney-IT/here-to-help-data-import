class FakeCreateHelpRequest:
    def __init__(self):
        self.received_help_requests = []

    def execute(self, help_requests):
        self.received_help_requests += help_requests
        response = {'created_help_request_ids': [len(self.received_help_requests)]}
        return response

    def get_returned_id(self):
        return len(self.received_help_requests)
