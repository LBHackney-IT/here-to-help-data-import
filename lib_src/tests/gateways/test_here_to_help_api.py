from urllib.error import HTTPError
import os
from dotenv import load_dotenv
from lib_src.lib.gateways.here_to_help_api import HereToHelpGateway
import datetime

load_dotenv()
os.environ['CV_19_RES_SUPPORT_V3_HELP_REQUESTS_BASE_URL'] = "localhost:3000/"


class TestCreateHelpRequest:

    def setup_method(self, method):
        self.POST_HELP_REQUESTS_URL = "localhost:3000/v3/help-requests"
        self.gateway = HereToHelpGateway()

    def test(self, requests_mock):
        requests_mock.register_uri(
            'POST',
            self.POST_HELP_REQUESTS_URL,
            text='{"Id": "1"}')
        assert self.gateway.create_help_request(help_request={}) == {"Id": "1"}

    def test_authentication_error_handling(self, requests_mock):
        requests_mock.register_uri(
            'POST',
            self.POST_HELP_REQUESTS_URL,
            exc=HTTPError(
                url="",
                code=403,
                msg="Forbidden",
                hdrs={},
                fp=None))
        assert self.gateway.create_help_request(
            help_request={})["Error"] == "Forbidden"

    def test_other_http_error_handling(self, requests_mock):
        requests_mock.register_uri(
            'POST',
            self.POST_HELP_REQUESTS_URL,
            exc=HTTPError(
                url="",
                code=500,
                msg="Connection error",
                hdrs={},
                fp=None))
        assert self.gateway.create_help_request(
            help_request={})["Error"] == "Connection error"

    def test_general_error_handling(self, requests_mock):
        requests_mock.register_uri(
            'POST',
            self.POST_HELP_REQUESTS_URL,
            exc=Exception("Exception"))
        assert self.gateway.create_help_request(
            help_request={})["Error"] is not None

    def test_handle_non_json_responses(self, requests_mock):
        requests_mock.register_uri(
            'POST', self.POST_HELP_REQUESTS_URL, text="{{}")
        assert self.gateway.create_help_request(
            help_request={})["Error"] is not None


class TestGetHelpRequest:

    def setup_method(self, method):
        self.GET_URL = "localhost:3000/v3/help-requests/50"
        self.gateway = HereToHelpGateway()

    def test(self, requests_mock):
        dirname = os.path.dirname(__file__)

        with open(os.path.join(dirname, '../fixture.json'), 'r') as file:
            mock_response = file.read()

        requests_mock.register_uri('GET', self.GET_URL, text=mock_response)

        response = self.gateway.get_help_request(help_request_id=50)
        assert response == {
            "Id": 50,
            "ResidentId": 1162,
            "IsOnBehalf": None,
            "ConsentToCompleteOnBehalf": None,
            "OnBehalfFirstName": None,
            "OnBehalfLastName": None,
            "OnBehalfEmailAddress": None,
            "OnBehalfContactNumber": None,
            "RelationshipWithResident": None,
            "Postcode": "YF2 9MI",
            "Uprn": "5088439290",
            "Ward": None,
            "AddressFirstLine": "30",
            "AddressSecondLine": "Morningstar",
            "AddressThirdLine": "Yasothon",
            "GettingInTouchReason": None,
            "HelpWithAccessingFood": None,
            "HelpWithAccessingSupermarketFood": None,
            "HelpWithCompletingNssForm": None,
            "HelpWithShieldingGuidance": None,
            "HelpWithNoNeedsIdentified": None,
            "HelpWithAccessingMedicine": None,
            "HelpWithAccessingOtherEssentials": None,
            "HelpWithDebtAndMoney": None,
            "HelpWithHealth": None,
            "HelpWithMentalHealth": None,
            "HelpWithAccessingInternet": None,
            "HelpWithHousing": None,
            "HelpWithJobsOrTraining": None,
            "HelpWithChildrenAndSchools": None,
            "HelpWithDisabilities": None,
            "HelpWithSomethingElse": True,
            "MedicineDeliveryHelpNeeded": None,
            "IsPharmacistAbleToDeliver": None,
            "WhenIsMedicinesDelivered": None,
            "NameAddressPharmacist": None,
            "UrgentEssentials": None,
            "UrgentEssentialsAnythingElse": None,
            "CurrentSupport": None,
            "CurrentSupportFeedback": None,
            "FirstName": "Natalee",
            "LastName": "Landon",
            "DobMonth": "4",
            "DobYear": "2013",
            "DobDay": "3",
            "ContactTelephoneNumber": "4338718059",
            "ContactMobileNumber": "5486383574",
            "EmailAddress": "nlandon7@flickr.com",
            "GpSurgeryDetails": None,
            "NumberOfChildrenUnder18": None,
            "ConsentToShare": None,
            "DateTimeRecorded": "2021-02-17T09:29:24.814513",
            "RecordStatus": None,
            "InitialCallbackCompleted": None,
            "CallbackRequired": True,
            "CaseNotes": [{'author': 'Data Ingestion: National Shielding Service System '
                                     'list',
                           'note': 'CEV: Dec 2020 Tier 4 NSSS Submitted on:  '
                                   '2020-04-30T22:46:43Z. Do you want supermarket '
                                   'deliveries? No. Do you have someone to go shopping '
                                   'for you? No. Do you need someone to contact you about '
                                   'local support? Yes.',
                           'noteDate': ' Thu, 18 Feb 2021 12:16:21 '},
                          {'author': 'J. Cole',
                           'note': 'Ut facile earum sensus appareat. quod in homine '
                                   'multo.',
                           'noteDate': 'Thu, 18 Feb 2021 14:11:51 GMT'}],
            "AdviceNotes": None,
            "HelpNeeded": "Shielding",
            "NhsNumber": "7919366992",
            "NhsCtasId": None,
            "AssignedTo": None,
            "Metadata": {
                "nsss_id": "a00c886c-6994-45ce-92f0-dc64fe8f631c"
            },
            "HelpRequestCalls": []}

    #
    # "[{'author': 'Data Ingestion: Shielding Patient List', 'noteDate': 'Tue, 23 Feb 2021 15:18:33 ', 'note': 'SPL Category: No change to current status.'}]"

    def test_authentication_error_handling(self, requests_mock):
        requests_mock.register_uri(
            'GET',
            self.GET_URL,
            exc=HTTPError(
                url="",
                code=403,
                msg="Forbidden",
                hdrs={},
                fp=None))
        assert self.gateway.get_help_request(
            help_request_id=50)["Error"] == "Forbidden"

    def test_other_http_error_handling(self, requests_mock):
        requests_mock.register_uri(
            'GET',
            self.GET_URL,
            exc=HTTPError(
                url="",
                code=500,
                msg="Connection error",
                hdrs={},
                fp=None))
        assert self.gateway.get_help_request(
            help_request_id=50)["Error"] == "Connection error"

    def test_general_error_handling(self, requests_mock):
        requests_mock.register_uri(
            'GET', self.GET_URL, exc=Exception("Exception"))
        assert self.gateway.get_help_request(help_request_id=50)[
            "Error"] is not None

    def test_handle_non_json_responses(self, requests_mock):
        requests_mock.register_uri('GET', self.GET_URL, text="{{}}")
        assert self.gateway.get_help_request(help_request_id=50)[
            "Error"] is not None


class TestCreateCaseNote:
    def setup_method(self, method):
        self.POST_CASE_NOTES_URL = 'localhost:3000/v4/residents/2/help-requests/3/case-notes'
        self.gateway = HereToHelpGateway()

    def test(self, requests_mock):
        requests_mock.register_uri(
            'POST',
            self.POST_CASE_NOTES_URL,
            text='{"Id": "1"}')

        result = self.gateway.create_case_note(
            case_note={
                "author": "Ben",
                "note": "Hello again",
            },
            resident_id=2,
            help_request_id=3)

        note_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")

        assert requests_mock.last_request.text == '{"CaseNote": "{\\"author\\": \\"Ben\\", \\"noteDate\\": \\"' + \
            note_date + '\\", \\"note\\": \\"Hello again\\"}"}'

        assert result == {
            "Id": "1"}

    def test_authentication_error_handling(self, requests_mock):
        requests_mock.register_uri(
            'POST',
            self.POST_CASE_NOTES_URL,
            exc=HTTPError(
                url="",
                code=403,
                msg="Forbidden",
                hdrs={},
                fp=None))
        assert self.gateway.create_case_note(
            case_note={
                "author": "Name",
                "note": "note",
            },
            resident_id=2,
            help_request_id=3)["Error"] == "Forbidden"

    def test_other_http_error_handling(self, requests_mock):
        requests_mock.register_uri(
            'POST',
            self.POST_CASE_NOTES_URL,
            exc=HTTPError(
                url="",
                code=500,
                msg="Connection error",
                hdrs={},
                fp=None))
        assert self.gateway.create_case_note(
            case_note={
                "author": "Name",
                "note": "note",
            },
            resident_id=2,
            help_request_id=3)["Error"] == "Connection error"

    def test_general_error_handling(self, requests_mock):
        requests_mock.register_uri(
            'POST',
            self.POST_CASE_NOTES_URL,
            exc=Exception("Exception"))
        assert self.gateway.create_case_note(
            case_note={
                "author": "Name",
                "caseNote": "note"},
            resident_id=2,
            help_request_id=3)["Error"] is not None

    def test_handle_non_json_responses(self, requests_mock):
        requests_mock.register_uri(
            'POST', self.POST_CASE_NOTES_URL, text="{{}")
        assert self.gateway.create_case_note(
            case_note={
                "author": "Name",
                "caseNote": "note"},
            resident_id=2,
            help_request_id=3)["Error"] is not None
