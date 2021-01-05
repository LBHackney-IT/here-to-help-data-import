from create_help_requests import CreateHelpRequest


class FakeHereToHelpGateway:
    def __init__(self, error=False):
        self.count = 0
        self.error = error

    def create_help_request(self, help_request):
        if self.error:
            raise Exception("message")
        self.count += 1
        if 'FirstName' in help_request:
            return {"Id": self.count}
        else:
            return {"Error": "error message"}


def test_create_help_request():
    gateway = FakeHereToHelpGateway()

    requests = [{"FirstName": "James", "LastName": "Smith", "NhsNumber": "123"},
                {"FirstName": "Jane", "LastName": "Doe", "NhsNumber": "321"},
                {"LastName": "Jones", "EmailAddress": "sample@example.com"}]

    use_case = CreateHelpRequest(gateway=gateway)
    result = use_case.execute(help_requests=requests)
    assert result["created_help_request_ids"] == [1, 2]
    assert result["unsuccessful_help_requests"][0]["EmailAddress"] == "sample@example.com"
    assert result["unsuccessful_help_requests"][0]["Error"] == "error message"
    assert gateway.count == 3


def test_create_help_request_with_error():
    gateway = FakeHereToHelpGateway(error=True)

    help_requests = [{"FirstName": "James", "LastName": "Smith", "NhsNumber": "123"},
                     {"FirstName": "Jane", "LastName": "Doe", "NhsNumber": "321"},
                     {"LastName": "Jones", "EmailAddress": "sample@example.com"}]
    use_case = CreateHelpRequest(gateway=gateway)
    initial_help_requests = []
    for help_request in help_requests:
        initial_help_requests.append(help_request.copy())
    for help_request in initial_help_requests:
        help_request["Error"] = "message"
    result = use_case.execute(help_requests)

    assert result == {"created_help_request_ids": [], "unsuccessful_help_requests": [],
                      "exceptions": initial_help_requests}
