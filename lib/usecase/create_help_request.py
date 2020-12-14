import json


class CreateHelpRequest:

    def __init__(self, gateway):
        self.gateway = gateway

    def execute(self, help_request):
        return self.gateway.create_help_request(help_request=help_request)
