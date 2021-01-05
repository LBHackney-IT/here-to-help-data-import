class LambdaHandler:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request

    def execute(self, event, context):
        help_request = [
            {
                "IsOnBehalf": False,
                "ConsentToCompleteOnBehalf": False,
                "OnBehalfFirstName": "Test",
                "OnBehalfLastName": "Test",
                "OnBehalfEmailAddress": "Test",
                "OnBehalfContactNumber": "Test",
                "RelationshipWithResident": "Test",
                "PostCode": "Test",
                "Uprn": "TestToo",
                "Ward": "Test",
                "AddressFirstLine": "Test",
                "AddressSecondLine": "Test",
                "AddressThirdLine": "Test",
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
                "FirstName": "LambdaTest1",
                "LastName": "LambdaTest1",
                "DobMonth": "Test",
                "DobYear": "Test",
                "DobDay": "Test",
                "ContactTelephoneNumber": "Test",
                "ContactMobileNumber": "Test",
                "EmailAddress": "Test",
                "GpSurgeryDetails": "Test",
                "NumberOfChildrenUnder18": "Test",
                "ConsentToShare": False,
                "DateTimeRecorded": "2020-07-23T00:00:00",
                "RecordStatus": "MASTER",
                "InitialCallbackCompleted": None,
                "CallbackRequired": True,
                "CaseNotes": None,
                "AdviceNotes": None,
                "HelpNeeded": "Conact Tracing"
            }
        ]
        # get the files
        # clean the files
        # help_request=get the format that we need
        # we need to add tests around the lambda handler

        response = self.create_help_request.execute(help_requests=help_request)
        return response
