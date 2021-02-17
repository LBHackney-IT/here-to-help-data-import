from urllib.error import HTTPError
from here_to_help_api import HereToHelpGateway
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL'] = "localhost:3000/"
url = os.getenv("CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL")+"v3/help-requests"
gateway = HereToHelpGateway()


def test_create_help_request(requests_mock):
    requests_mock.register_uri('POST', url, text='{"Id": "1"}')
    assert gateway.create_help_request(help_request={}) == {"Id": "1"}


def test_create_help_request_authentication_error_handling(requests_mock):
    requests_mock.register_uri('POST', url, exc=HTTPError(url="", code=403, msg="Forbidden", hdrs={}, fp=None))
    assert gateway.create_help_request(help_request={})["Error"] == "Forbidden"


def test_create_help_request_other_http_error_handling(requests_mock):
    requests_mock.register_uri('POST', url, exc=HTTPError(url="", code=500, msg="Connection error", hdrs={}, fp=None))
    assert gateway.create_help_request(help_request={})["Error"] == "Connection error"


def test_create_help_request_general_error_handling(requests_mock):
    requests_mock.register_uri('POST', url, exc=Exception("Exception"))
    assert gateway.create_help_request(help_request={})["Error"] is not None


def test_create_help_request_handle_non_json_responses(requests_mock):
    requests_mock.register_uri('POST', url, text="{{}")
    assert gateway.create_help_request(help_request={})["Error"] is not None

def test_get_help_request(requests_mock):
    url = os.getenv("CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL")+"v3/help-requests/50"

    dirname = os.path.dirname(__file__)

    with open(os.path.join(dirname, 'fixture.json'), 'r') as file:
        mock_response = file.read()

    requests_mock.register_uri('GET', url, text=mock_response)

    assert gateway.get_help_request(help_request_id=50) == {
  "Id": 50,
  "ResidentId": 0,
  "IsOnBehalf": True,
  "ConsentToCompleteOnBehalf": True,
  "OnBehalfFirstName": "string",
  "OnBehalfLastName": "string",
  "OnBehalfEmailAddress": "string",
  "OnBehalfContactNumber": "string",
  "RelationshipWithResident": "string",
  "Postcode": "string",
  "Uprn": "string",
  "Ward": "string",
  "AddressFirstLine": "string",
  "AddressSecondLine": "string",
  "AddressThirdLine": "string",
  "GettingInTouchReason": "string",
  "HelpWithAccessingFood": True,
  "HelpWithAccessingSupermarketFood": True,
  "HelpWithCompletingNssForm": True,
  "HelpWithShieldingGuidance": True,
  "HelpWithNoNeedsIdentified": True,
  "HelpWithAccessingMedicine": True,
  "HelpWithAccessingOtherEssentials": True,
  "HelpWithDebtAndMoney": True,
  "HelpWithHealth": True,
  "HelpWithMentalHealth": True,
  "HelpWithAccessingInternet": True,
  "HelpWithHousing": True,
  "HelpWithJobsOrTraining": True,
  "HelpWithChildrenAndSchools": True,
  "HelpWithDisabilities": True,
  "HelpWithSomethingElse": True,
  "MedicineDeliveryHelpNeeded": True,
  "IsPharmacistAbleToDeliver": True,
  "WhenIsMedicinesDelivered": "string",
  "NameAddressPharmacist": "string",
  "UrgentEssentials": "string",
  "UrgentEssentialsAnythingElse": "string",
  "CurrentSupport": "string",
  "CurrentSupportFeedback": "string",
  "FirstName": "string",
  "LastName": "string",
  "DobMonth": "string",
  "DobYear": "string",
  "DobDay": "string",
  "ContactTelephoneNumber": "string",
  "ContactMobileNumber": "string",
  "EmailAddress": "string",
  "GpSurgeryDetails": "string",
  "NumberOfChildrenUnder18": "string",
  "ConsentToShare": True,
  "DateTimeRecorded": "2021-02-17T16:14:40.351Z",
  "RecordStatus": "string",
  "InitialCallbackCompleted": True,
  "CallbackRequired": True,
  "CaseNotes": "string",
  "AdviceNotes": "string",
  "HelpNeeded": "string",
  "NhsNumber": "string",
  "NhsCtasId": "string",
  "AssignedTo": "string",
  "HelpRequestCalls": [
    {
      "Id": 0,
      "HelpRequestId": 0,
      "CallType": "string",
      "CallDirection": "string",
      "CallOutcome": "string",
      "CallDateTime": "2021-02-17T16:14:40.351Z",
      "CallHandler": "string"
    }
  ]
}
