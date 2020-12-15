from urllib.error import HTTPError
from here_to_help_api import HereToHelpGateway
from dotenv import load_dotenv
import os

load_dotenv()
gateway = HereToHelpGateway()
url = os.getenv("CV-19-RES-SUPPORT-V3-HELP-REQUESTS-URL")


def test_create_help_request(requests_mock):
    requests_mock.post(url, text='[{"id": "1"}]')
    help_request = {}
    assert gateway.create_help_request(help_request=help_request) == [{"id": "1"}]


def test_create_help_request_authentication_error_handling(requests_mock):
    requests_mock.register_uri('POST', url, exc=HTTPError(url="", code=403, msg="", hdrs={}, fp=None))
    help_request = {}
    assert gateway.create_help_request(help_request=help_request) == {}


def test_create_help_request_other_http_error_handling(requests_mock):
    requests_mock.register_uri('POST', url, exc=HTTPError(url="", code=500, msg="", hdrs={}, fp=None))
    help_request = {}
    assert gateway.create_help_request(help_request=help_request) == {}


def test_create_help_request_general_error_handling(requests_mock):
    requests_mock.register_uri('POST', url, exc=ValueError)
    help_request = {}
    assert gateway.create_help_request(help_request=help_request) == {}
