from urllib.error import HTTPError
from here_to_help_api import HereToHelpGateway
from dotenv import load_dotenv
import os

load_dotenv()
gateway = HereToHelpGateway()
os.environ['CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL'] = "localhost:3000/"
url = os.getenv("CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL")+"v3/help-requests"


def test_create_help_request(requests_mock):
    requests_mock.register_uri('POST', url, text='{"Id": "1"}')
    assert gateway.create_help_request(help_request={}) == {"Id": "1"}


def test_create_help_request_authentication_error_handling(requests_mock):
    requests_mock.register_uri('POST', url, exc=HTTPError(url="", code=403, msg="Forbidden", hdrs={}, fp=None))
    assert gateway.create_help_request(help_request={})["Error"] == "Forbidden"


def test_create_help_request_other_http_error_handling(requests_mock):
    requests_mock.register_uri('POST', url, exc=HTTPError(url="", code=500, msg="Connection error", hdrs={}, fp=None))
    assert gateway.create_help_request(help_request={})["Error"] == "Connection error"


def test_create_help_request_general_error_handling(requests_mock):
    requests_mock.register_uri('POST', url, exc=Exception("Exception"))
    assert gateway.create_help_request(help_request={})["Error"] is not None


def test_create_help_request_handle_non_json_responses(requests_mock):
    requests_mock.register_uri('POST', url, text="{{}")
    assert gateway.create_help_request(help_request={})["Error"] is not None
