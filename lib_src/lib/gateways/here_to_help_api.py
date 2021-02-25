import os
from urllib.error import HTTPError
import datetime

import requests
import json
from dotenv import load_dotenv

load_dotenv()


class HereToHelpGateway:
    def __init__(self):
        self.base_url = os.getenv(
            "CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL")
        self.api_key = os.getenv("CV_19_RES_SUPPORT_V3_HELP_REQUESTS_API_KEY")
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

    def create_help_request(self, help_request):
        try:
            help_requests_url = f'{self.base_url}v3/help-requests'

            data = json.dumps(help_request)
            response = requests.request(
                "POST", help_requests_url, headers=self.headers, data=data)
            if response.status_code == 403:
                print("Authentication error", response)
                return {"Error": json.dumps(response.json())}

            result = eval(response.text)

        except HTTPError as err:
            print(
                "Could not create a new help request: ",
                help_request,
                err.msg)
            return {"Error": err.msg}
        except Exception as err:
            print("Help request was not created", help_request)
            return {"Error": err}

        return result

    def get_help_request(self, help_request_id):
        try:
            help_requests_url = f'{self.base_url}v3/help-requests/{help_request_id}'

            response = requests.request(
                "GET", help_requests_url, headers=self.headers)

            if response.status_code == 403:
                print("Authentication error", response)
                return {"Error": json.dumps(response.json())}

            result = json.loads(response.text)
            try:
                result["CaseNotes"] = json.loads(result["CaseNotes"])
            except Exception as err:
                print('cant parse case notes: ', err)
                result["CaseNotes"] = {}

            result["Metadata"] = json.loads(
                result["Metadata"]) if result["Metadata"] else {}

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

            note_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")

            case_note = "\"{\\\"author\\\": \\\"" + case_note["author"] + "\\\", \\\"noteDate\\\": \\\"" + \
                        note_date + "\\\", \\\"note\\\": \\\"" + case_note["note"] + "\\\"}\""

            body = '{"CaseNote": ' + case_note + '}'

            response = requests.request(
                "POST", help_requests_url, headers=self.headers, data=body)
            if response.status_code == 403:
                print("Authentication error", response)
                return {"Error": json.dumps(response.json())}

            result = eval(response.text)

        except HTTPError as err:
            print("Could not create case not: ", case_note, err.msg)
            return {"Error": err.msg}
        except Exception as err:
            print("Case note was not created", case_note)
            return {"Error": err}

        return result
