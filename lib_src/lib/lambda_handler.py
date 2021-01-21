from faker import Faker
import datetime

class LambdaHandler:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request
        self.fake = Faker(['en-GB', 'en_GB', 'en_GB', 'en-GB'])

    def execute(self, event, context):
        help_request = [
            {
                "IsOnBehalf": False,
                "ConsentToCompleteOnBehalf": False,
                "OnBehalfFirstName": "",
                "OnBehalfLastName": "",
                "OnBehalfEmailAddress": "",
                "OnBehalfContactNumber": "",
                "RelationshipWithResident": "",
                "PostCode": self.fake.postcode(),
                "Uprn": "",
                "Ward": "",
                "AddressFirstLine": self.fake.street_address(),
                "AddressSecondLine": "",
                "AddressThirdLine": "",
                "GettingInTouchReason": "Test",
                "HelpWithAccessingFood": False,
                "HelpWithAccessingSupermarketFood": False,
                "HelpWithCompletingNssForm": False,
                "HelpWithShieldingGuidance": False,
                "HelpWithNoNeedsIdentified": True,
                "HelpWithAccessingMedicine": False,
                "HelpWithAccessingOtherEssentials": False,
                "HelpWithDebtAndMoney": False,
                "HelpWithHealth": False,
                "HelpWithMentalHealth": False,
                "HelpWithAccessingInternet": False,
                "HelpWithHousing": None,
                "HelpWithJobsOrTraining": None,
                "HelpWithChildrenAndSchools": None,
                "HelpWithDisabilities": None,
                "HelpWithSomethingElse": None,
                "MedicineDeliveryHelpNeeded": None,
                "IsPharmacistAbleToDeliver": False,
                "WhenIsMedicinesDelivered": "Test",
                "NameAddressPharmacist": "Test",
                "UrgentEssentials": "Test",
                "UrgentEssentialsAnythingElse": "This is a newly added db field",
                "CurrentSupport": "Test",
                "CurrentSupportFeedback": "Test",
                "FirstName": "Test: %s" % self.fake.first_name(),
                "LastName": "Test: %s" % self.fake.last_name(),
                "DobMonth": self.fake.month(),
                "DobYear": self.fake.year(),
                "DobDay": self.fake.day_of_month(),
                "ContactTelephoneNumber": self.fake.phone_number(),
                "ContactMobileNumber": self.fake.cellphone_number(),
                "EmailAddress": self.fake.free_email(),
                "GpSurgeryDetails": "Test",
                "NumberOfChildrenUnder18": 0,
                "ConsentToShare": False,
                "DateTimeRecorded": datetime.datetime.utcnow().isoformat(),
                "RecordStatus": "MASTER",
                "InitialCallbackCompleted": None,
                "CallbackRequired": True,
                "CaseNotes": None,
                "AdviceNotes": None,
                "HelpNeeded": "Contact Tracing"
            }
        ]
        # get the files
        # clean the files
        # help_request=get the format that we need
        # we need to add tests around the lambda handler

        response = self.create_help_request.execute(help_requests=help_request)
        return response
