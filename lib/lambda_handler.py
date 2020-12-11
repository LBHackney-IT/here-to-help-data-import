class LambdaHandler:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request

    def execute(self, event, context):
        response = self.create_help_request.execute()
        return response
