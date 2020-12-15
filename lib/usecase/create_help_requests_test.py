from create_help_requests import CreateHelpRequest
import json

class FakeHereToHelpGateway:
    def __init__(self):
        self.count = 0

    def create_help_request(self, help_request):
        self.count += 1
        if 'FirstName' in help_request:
            return json.loads(f'{{"id": {self.count}}}')
        else:
            return None


gateway = FakeHereToHelpGateway()


def test_create_help_request():
    help_requests = [   {"FirstName": "James", "LastName": "Smith", "NhsNumber": "123"},
                        {"FirstName": "Jane", "LastName": "Doe", "NhsNumber": "321"},
                        {"LastName": "Jones", "EmailAddress": "sample@example.com"}]
    usecase = CreateHelpRequest(gateway=gateway)
    result = usecase.execute(help_requests=help_requests)
    assert result == {"created_help_request_ids": [1, 2], "unsuccessful_help_requests": [{"LastName": "Jones", "EmailAddress": "sample@example.com"}]}
    assert gateway.count == 3
