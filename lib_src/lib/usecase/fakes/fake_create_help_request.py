class FakeCreateHelpRequest:
    def __init__(self):
        self.received_help_requests = []

    def execute(self, help_requests):
        self.received_help_requests += help_requests
