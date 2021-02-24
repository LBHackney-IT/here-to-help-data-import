from faker import Faker

class FakeHereToHelpGateway:
    def __init__(self, error=False, test_resident_id=1162, test_case_note=""):
        self.fake = Faker(['en-GB', 'en_GB', 'en_GB', 'en-GB'])

        self.count = 0
        self.error = error
        self.resident_id = test_resident_id
        self.case_note = test_case_note
        self.get_help_request_called_with = []
        self.create_case_note_called_with = []

    def create_help_request(self, help_request):
        if self.error:
            raise Exception("message")
        self.count += 1
        if 'FirstName' in help_request:
            return {"Id": self.count}
        else:
            return {"Error": "error message"}

    def get_help_request(self, help_request_id):
        self.get_help_request_called_with.append(help_request_id)

        return {
            "Id": help_request_id,
            "ResidentId": self.resident_id,
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
            "CaseNotes": [{
                "author": "Data Ingestion: National Shielding Service System list",
                "noteDate": " Wed, 17 Feb 2021 09:29:24 ",
                "note": self.case_note if self.case_note else self.fake.sentence()}],
            "AdviceNotes": None,
            "HelpNeeded": "Shielding",
            "NhsNumber": "7919366992",
            "NhsCtasId": None,
            "AssignedTo": None,
            "Metadata": {
                "nsss_id": "a00c886c-6994-45ce-92f0-dc64fe8f631c"},
            "HelpRequestCalls": []}

    def create_case_note(self, resident_id, help_request_id, case_note):
        self.create_case_note_called_with.append({
            'resident_id': resident_id,
            'help_request_id': help_request_id,
            'case_note': case_note
        })
