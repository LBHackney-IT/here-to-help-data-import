import os
from urllib.error import HTTPError

import requests
import json
from dotenv import load_dotenv

load_dotenv()


class HereToHelpGateway:

    def create_help_request(self, help_request):
        try:
            help_requests_url = os.getenv("CV_19_RES_SUPPORT_V3_HELP_REQUESTS_URL")
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", help_requests_url, headers=headers, data=help_request)
            result = json.loads(response.text)
            print(response.text)
        except HTTPError as err:
            if err.code == 403:
                print("Authentication error", err.msg)
                return {"Error": err.msg}
            else:
                print("Could not create a new help request: ", help_request, err.msg)
                return {"Error": err.msg}
        except Exception as err:
            print("Help request was not created", help_request)
            return {"Error": err}

        return result
