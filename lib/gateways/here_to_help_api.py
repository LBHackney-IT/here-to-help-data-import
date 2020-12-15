import os
from urllib.error import HTTPError

import requests
import json
from dotenv import load_dotenv

load_dotenv()


class HereToHelpGateway:

    def create_help_request(self, help_request):
        try:
            help_requests_url = os.getenv("CV-19-RES-SUPPORT-V3-HELP-REQUESTS-URL")
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", help_requests_url, headers=headers, data=help_request)
            print(response.text.encode('utf8'))
        except HTTPError as err:
            if err.code == 403:
                print("Authentication error", err.msg)
                return {}
            else:
                print("Could not create a new help request: ", help_request, err.msg)
                return {}
        except:
            print("Could not create a new help request: ", help_request)
            return {}

        return json.loads(response.text)
