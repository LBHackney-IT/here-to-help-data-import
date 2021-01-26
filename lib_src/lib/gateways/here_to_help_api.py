import os
from urllib.error import HTTPError

import requests
import json
from dotenv import load_dotenv

load_dotenv()


class HereToHelpGateway:

    def create_help_request(self, help_request):
        try:
            help_requests_url = os.getenv("CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL")+"v3/help-requests"
            help_requests_api_key = os.getenv("CV_19_RES_SUPPORT_V3_HELP_REQUESTS_API_KEY")
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': help_requests_api_key
            }
            data = json.dumps(help_request)
            response = requests.request("POST", help_requests_url, headers=headers, data=data)
            if response.status_code == 403:
                print("Authentication error", response)
                return {"Error": json.dumps(response.json())}
            print("Response from the backend", response.text)
            result = eval(response.text)
            print("Evaluated result", result)
        except HTTPError as err:
            print("Could not create a new help request: ", help_request, err.msg)
            return {"Error": err.msg}
        except Exception as err:
            print("Help request was not created", help_request)
            return {"Error": err}

        return result
