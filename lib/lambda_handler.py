class LambdaHandler:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request

    def execute(self, event, context):
        help_request = {}
        response = self.create_help_request.execute(help_request=help_request)
        return response
