from lib_src.lib.usecase.create_help_requests import CreateHelpRequest
from lib_src.tests.fakes.fake_here_to_help_gateway import FakeHereToHelpGateway

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
