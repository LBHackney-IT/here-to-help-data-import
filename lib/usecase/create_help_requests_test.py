from create_help_requests import CreateHelpRequest
import json

class FakeHereToHelpGateway:
    def __init__(self,error=False):
        self.count = 0
        self.error = error

    def create_help_request(self, help_request):
        if(self.error):
            raise Exception("message")
        self.count += 1
        if 'FirstName' in help_request:
            return json.loads(f'{{"id": {self.count}}}')
        else:
            return None


def test_create_help_request():
    gateway = FakeHereToHelpGateway()

    help_requests = [   {"FirstName": "James", "LastName": "Smith", "NhsNumber": "123"},
                        {"FirstName": "Jane", "LastName": "Doe", "NhsNumber": "321"},
                        {"LastName": "Jones", "EmailAddress": "sample@example.com"}]
    usecase = CreateHelpRequest(gateway=gateway)
    result = usecase.execute(help_requests=help_requests)
    assert result == {"created_help_request_ids": [1, 2], "unsuccessful_help_requests": [{"LastName": "Jones", "EmailAddress": "sample@example.com"}]}
    assert gateway.count == 3

def test_create_help_request_with_error():
    gateway = FakeHereToHelpGateway(error=True)

    help_requests = [   {"FirstName": "James", "LastName": "Smith", "NhsNumber": "123"},
                        {"FirstName": "Jane", "LastName": "Doe", "NhsNumber": "321"},
                        {"LastName": "Jones", "EmailAddress": "sample@example.com"}]
    usecase = CreateHelpRequest(gateway=gateway)
    result = usecase.execute(help_requests=help_requests)
    assert result == {"created_help_request_ids": [], "unsuccessful_help_requests": [], "exceptions": help_requests}