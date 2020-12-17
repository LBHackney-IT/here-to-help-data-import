class LambdaHandler:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request

    def execute(self, event, context):
        help_request = [{}]
        # get the files
        # clean the files
        # help_request=get the format that we need

        response = self.create_help_request.execute(help_request=help_request)
        return response
