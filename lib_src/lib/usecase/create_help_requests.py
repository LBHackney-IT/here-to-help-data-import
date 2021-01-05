class CreateHelpRequest:

    def __init__(self, gateway):
        self.gateway = gateway

    def execute(self, help_requests):
        result = {"created_help_request_ids": [], "unsuccessful_help_requests": []}
        exceptions = []
        for help_request in help_requests:
            try:
                response = self.gateway.create_help_request(help_request=help_request)
                if "Error" in response:
                    help_request['Error'] = response["Error"]
                    result["unsuccessful_help_requests"].append(help_request)
                else:
                    result["created_help_request_ids"].append(response['Id'])
            except Exception as err:
                help_request['Error'] = str(err)
                exceptions.append(help_request)
                print("[CreateHelpRequestUseCase] Failed to create help request", str(err), help_request)
            if exceptions:
                result["exceptions"] = exceptions
        return result
