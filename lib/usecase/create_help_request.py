import json


class CreateHelpRequest:

    def execute(self):
        print("hello world")

        response = json.dumps({
            "success": True,
        })
        return response
