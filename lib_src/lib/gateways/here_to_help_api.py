import os
from urllib.error import HTTPError

import requests
import json
from dotenv import load_dotenv

load_dotenv()


class HereToHelpGateway:
    def __init__(self):
        self.base_url = os.getenv("CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL")
        self.api_key = os.getenv("CV_19_RES_SUPPORT_V3_HELP_REQUESTS_API_KEY")

    def create_help_request(self, help_request):
        try:
            help_requests_url = f'{self.base_url}v3/help-requests'
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.api_key
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

    def get_help_request(self, help_request_id):
        try:
            help_requests_url = f'{self.base_url}v3/help-requests/{help_request_id}'
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.api_key
            }
            response = requests.request("GET", help_requests_url, headers=headers)
            
            if response.status_code == 403:
                print("Authentication error", response)
                return {"Error": json.dumps(response.json())}

            print("Response from the backend", response.text)
            result = json.loads(response.text)
            result["CaseNotes"] = json.loads(result["CaseNotes"]) if result["CaseNotes"] else {}
            result["Metadata"] = json.loads(result["Metadata"]) if result["Metadata"] else {}

            print("Evaluated result", result)
        except HTTPError as err:
            print("Could not get help request id: ", help_request_id, err.msg)
            return {"Error": err.msg}
        except Exception as err:
            print("Help request was not found", help_request_id)
            return {"Error": err}

        return result


    def create_case_note(self, resident_id, help_request_id, case_note):
        try:
            help_requests_url = f'{self.base_url}v4/residents/{resident_id}/help-requests/{help_request_id}/case-notes'
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.api_key
            }
            data = json.dumps(case_note)
            response = requests.request("POST", help_requests_url, headers=headers, data=data)
            if response.status_code == 403:
                print("Authentication error", response)
                return {"Error": json.dumps(response.json())}
            print("Response from the backend", response.text)
            result = eval(response.text)
            print("Evaluated result", result)
        except HTTPError as err:
            print("Could not create case not: ", case_note, err.msg)
            return {"Error": err.msg}
        except Exception as err:
            print("Case note was not created", case_note)
            return {"Error": err}

        return result
