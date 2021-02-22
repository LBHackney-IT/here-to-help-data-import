class FakeCreateHelpRequest:
    def __init__(self):
        self.received_help_requests = []

    def execute(self, help_requests):
        self.received_help_requests += help_requests
        response = {'created_help_request_ids': [123]}
        return response
