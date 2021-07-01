from faker import Faker

class FakeHereToHelpGateway:
    def __init__(self, error=False, test_resident_id=1162, test_case_note="", cev_exists=True):
        self.fake = Faker(['en-GB', 'en_GB', 'en_GB', 'en-GB'])

        self.count = 0
        self.error = error
        self.resident_id = test_resident_id
        self.case_note = test_case_note
        self.get_help_request_called_with = []
        self.create_case_note_called_with = []
        self.get_multiple_help_requests_called_with = []
        self.create_resident_help_request_called_with = []
        self.cev_exists = cev_exists

    # Corresponds to old v3 endpoint (Resident + Help Request mix)
    def create_help_request(self, help_request):
        if self.error:
            raise Exception("message")
        self.count += 1
        if 'FirstName' in help_request:
            return {"Id": self.count}
        else:
            return {"Error": "error message"}

    # Corresponds to v4 endpoint - creates Help Request only.
    def create_resident_help_request(self, resident_id, help_request):
        args_dict = {
            'resident_id': resident_id,
            'help_request': help_request
        }
        
        self.create_resident_help_request_called_with.append(args_dict)

        return { 'Id': 1 }

    def get_resident_help_requests(self, resident_id):
        self.get_multiple_help_requests_called_with.append(resident_id)

        if self.cev_exists is False:
            return [{
                "Id": self.fake.random_number(digits=3),
                "ResidentId": resident_id,
                "IsOnBehalf": self.fake.null_boolean(),
                "ConsentToCompleteOnBehalf": self.fake.null_boolean(),
                "OnBehalfFirstName": self.fake.first_name(),
                "OnBehalfLastName": self.fake.last_name(),
                "OnBehalfEmailAddress": self.fake.free_email(),
                "OnBehalfContactNumber": self.fake.cellphone_number(),
                "RelationshipWithResident": None,
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
                "HelpWithSomethingElse": self.fake.boolean(),
                "MedicineDeliveryHelpNeeded": None,
                "WhenIsMedicinesDelivered": None,
                "UrgentEssentials": None,
                "UrgentEssentialsAnythingElse": None,
                "CurrentSupport": None,
                "CurrentSupportFeedback": None,
                "DateTimeRecorded": self.fake.date(),
                "InitialCallbackCompleted": None,
                "CallbackRequired": True,
                "CaseNotes": [{
                    "author": self.fake.name(),
                    "noteDate": self.fake.date(),
                    "note": self.case_note if self.case_note else self.fake.sentence()}],
                "AdviceNotes": None,
                "HelpNeeded": 'Welfare Call',
                "NhsCtasId": self.fake.uuid4(),
                "AssignedTo": self.fake.name(),
                "HelpRequestCalls": []}]

        return [{
            "Id": self.fake.random_number(digits=3),
            "ResidentId": resident_id,
            "IsOnBehalf": self.fake.null_boolean(),
            "ConsentToCompleteOnBehalf": self.fake.null_boolean(),
            "OnBehalfFirstName": self.fake.first_name(),
            "OnBehalfLastName": self.fake.last_name(),
            "OnBehalfEmailAddress": self.fake.free_email(),
            "OnBehalfContactNumber": self.fake.cellphone_number(),
            "RelationshipWithResident": None,
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
            "HelpWithSomethingElse": self.fake.boolean(),
            "MedicineDeliveryHelpNeeded": None,
            "WhenIsMedicinesDelivered": None,
            "UrgentEssentials": None,
            "UrgentEssentialsAnythingElse": None,
            "CurrentSupport": None,
            "CurrentSupportFeedback": None,
            "DateTimeRecorded": self.fake.date(),
            "InitialCallbackCompleted": None,
            "CallbackRequired": True,
            "CaseNotes": [{
                "author": self.fake.name(),
                "noteDate": self.fake.date(),
                "note": self.case_note if self.case_note else self.fake.sentence()}],
            "AdviceNotes": None,
            "HelpNeeded": 'Shielding',
            "NhsCtasId": self.fake.uuid4(),
            "AssignedTo": self.fake.name(),
            "HelpRequestCalls": []}]
    
    def get_help_request(self, help_request_id):
        self.get_help_request_called_with.append(help_request_id)

        return {
            "Id": help_request_id,
            "ResidentId": self.resident_id,
            "IsOnBehalf": self.fake.null_boolean(),
            "ConsentToCompleteOnBehalf": self.fake.null_boolean(),
            "OnBehalfFirstName": self.fake.first_name(),
            "OnBehalfLastName": self.fake.last_name(),
            "OnBehalfEmailAddress": self.fake.free_email(),
            "OnBehalfContactNumber": self.fake.cellphone_number(),
            "RelationshipWithResident": None,
            "Postcode": self.fake.postcode(),
            "Uprn": "5088439290",
            "Ward": None,
            "AddressFirstLine": self.fake.street_address(),
            "AddressSecondLine": "",
            "AddressThirdLine": "",
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
            "HelpWithSomethingElse": self.fake.boolean(),
            "MedicineDeliveryHelpNeeded": None,
            "IsPharmacistAbleToDeliver": None,
            "WhenIsMedicinesDelivered": None,
            "NameAddressPharmacist": None,
            "UrgentEssentials": None,
            "UrgentEssentialsAnythingElse": None,
            "CurrentSupport": None,
            "CurrentSupportFeedback": None,
            "FirstName": self.fake.first_name(),
            "LastName": self.fake.last_name(),
            "DobMonth": self.fake.month(),
            "DobYear": self.fake.year(),
            "DobDay": self.fake.day_of_month(),
            "ContactTelephoneNumber": self.fake.phone_number(),
            "ContactMobileNumber": self.fake.cellphone_number(),
            "EmailAddress": self.fake.free_email(),
            "GpSurgeryDetails": None,
            "NumberOfChildrenUnder18": None,
            "ConsentToShare": None,
            "DateTimeRecorded": self.fake.date(),
            "RecordStatus": None,
            "InitialCallbackCompleted": None,
            "CallbackRequired": True,
            "CaseNotes": [{
                "author": self.fake.name(),
                "noteDate": self.fake.date(),
                "note": self.case_note if self.case_note else self.fake.sentence()}],
            "AdviceNotes": None,
            "HelpNeeded": self.fake.random_sample(elements=('Shielding', 'Contact Tracing', 'Welfare'), length=1)[0],
            "NhsNumber": self.fake.numerify('############'),
            "NhsCtasId": self.fake.uuid4(),
            "AssignedTo": self.fake.name(),
            "Metadata": {
                "nsss_id": self.fake.uuid4()},
            "HelpRequestCalls": []}

    def create_case_note(self, resident_id, help_request_id, case_note):
        self.create_case_note_called_with.append({
            'resident_id': resident_id,
            'help_request_id': help_request_id,
            'case_note': case_note
        })
