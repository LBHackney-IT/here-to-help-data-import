class CreateHelpRequest:

    def __init__(self, gateway):
        self.gateway = gateway

    def execute(self, help_requests):
        ids = []
        unsuccessful = []
        for help_request in help_requests:
            result = self.gateway.create_help_request(help_request=help_request)
            if result is None:
                unsuccessful.append(help_request)
            else:
                ids.append(result["id"])
        return {"created_help_request_ids": ids, "unsuccessful_help_requests": unsuccessful}
