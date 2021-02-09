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
