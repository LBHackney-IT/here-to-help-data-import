from here_to_help_api import HereToHelpGateway

gateway = HereToHelpGateway()


def test_create_help_request():
    help_request = {}
    assert gateway.create_help_request(help_request=help_request) == {}
