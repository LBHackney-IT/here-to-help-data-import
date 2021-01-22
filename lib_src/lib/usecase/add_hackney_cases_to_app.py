class AddHackneyCasesToApp:
    def __init__(self, create_help_request):
        self.create_help_request = create_help_request

    def execute(self, data_frame):
        responses = []

        for index, row in data_frame.iterrows():
            row = row.to_dict()

            dob = row['Date of Birth'].split('/')

            dob_day = dob[0] if row['Date of Birth'] else ''
            dob_month = dob[1] if row['Date of Birth'] else ''
            dob_year = dob[2] if row['Date of Birth'] else ''
            print(row['Email'])

            help_request = [
                {
                    "IsOnBehalf": False,
                    "ConsentToCompleteOnBehalf": False,
                    "OnBehalfFirstName": "string",
                    "OnBehalfLastName": "string",
                    "OnBehalfEmailAddress": "string",
                    "OnBehalfContactNumber": "string",
                    "RelationshipWithResident": "string",
                    "Postcode": row['Email'],
                    "Uprn": "",
                    "Ward": "",
                    "AddressFirstLine": row['House Number'],
                    "AddressSecondLine": "",
                    "AddressThirdLine": "",
                    "GettingInTouchReason": "string",
                    "HelpWithAccessingFood": False,
                    "HelpWithAccessingSupermarketFood": False,
                    "HelpWithCompletingNssForm": False,
                    "HelpWithShieldingGuidance": False,
                    "HelpWithNoNeedsIdentified": False,
                    "HelpWithAccessingMedicine": False,
                    "HelpWithAccessingOtherEssentials": False,
                    "HelpWithDebtAndMoney": False,
                    "HelpWithHealth": False,
                    "HelpWithMentalHealth": False,
                    "HelpWithAccessingInternet": False,
                    "HelpWithHousing": False,
                    "HelpWithJobsOrTraining": False,
                    "HelpWithChildrenAndSchools": False,
                    "HelpWithDisabilities": False,
                    "HelpWithSomethingElse": True,
                    "MedicineDeliveryHelpNeeded": False,
                    "IsPharmacistAbleToDeliver": False,
                    "WhenIsMedicinesDelivered": "",
                    "NameAddressPharmacist": "",
                    "UrgentEssentials": "",
                    "UrgentEssentialsAnythingElse": "",
                    "CurrentSupport": "",
                    "CurrentSupportFeedback": "",
                    "FirstName": "Test: %s" % row["Forename"],
                    "LastName": "Test: %s" % row["Surname"],
                    "DobDay": dob_day,
                    "DobMonth": dob_month,
                    "DobYear": dob_year,
                    "ContactTelephoneNumber":  row["Phone"],
                    "ContactMobileNumber":  row["Phone2"],
                    "EmailAddress":  row["Email"],
                    "GpSurgeryDetails": "",
                    "NumberOfChildrenUnder18": "",
                    "ConsentToShare": False,
                    "RecordStatus": "",
                    "InitialCallbackCompleted": False,
                    "CallbackRequired": True,
                    "CaseNotes": row["Comments"],
                    "AdviceNotes": "",
                    "HelpNeeded": "Contact Tracing",
                    "NhsNumber": row["NHS Number"],
                    "NhsCtasId": row["Account ID"]
                }
            ]

            responses.append(self.create_help_request.execute(help_requests=help_request))

        # help_request = [
        #     {
        #         "IsOnBehalf": False,
        #         "ConsentToCompleteOnBehalf": False,
        #         "OnBehalfFirstName": "",
        #         "OnBehalfLastName": "",
        #         "OnBehalfEmailAddress": "",
        #         "OnBehalfContactNumber": "",
        #         "RelationshipWithResident": "",
        #         "PostCode": self.fake.postcode(),
        #         "Uprn": "",
        #         "Ward": "",
        #         "AddressFirstLine": self.fake.street_address(),
        #         "AddressSecondLine": "",
        #         "AddressThirdLine": "",
        #         "GettingInTouchReason": "Test",
        #         "HelpWithAccessingFood": False,
        #         "HelpWithAccessingSupermarketFood": False,
        #         "HelpWithCompletingNssForm": False,
        #         "HelpWithShieldingGuidance": False,
        #         "HelpWithNoNeedsIdentified": True,
        #         "HelpWithAccessingMedicine": False,
        #         "HelpWithAccessingOtherEssentials": False,
        #         "HelpWithDebtAndMoney": False,
        #         "HelpWithHealth": False,
        #         "HelpWithMentalHealth": False,
        #         "HelpWithAccessingInternet": False,
        #         "HelpWithHousing": None,
        #         "HelpWithJobsOrTraining": None,
        #         "HelpWithChildrenAndSchools": None,
        #         "HelpWithDisabilities": None,
        #         "HelpWithSomethingElse": None,
        #         "MedicineDeliveryHelpNeeded": None,
        #         "IsPharmacistAbleToDeliver": False,
        #         "WhenIsMedicinesDelivered": "Test",
        #         "NameAddressPharmacist": "Test",
        #         "UrgentEssentials": "Test",
        #         "UrgentEssentialsAnythingElse": "This is a newly added db field",
        #         "CurrentSupport": "Test",
        #         "CurrentSupportFeedback": "Test",
        #         "FirstName": "Test: %s" % self.fake.first_name(),
        #         "LastName": "Test: %s" % self.fake.last_name(),
        #         "DobMonth": self.fake.month(),
        #         "DobYear": self.fake.year(),
        #         "DobDay": self.fake.day_of_month(),
        #         "ContactTelephoneNumber": self.fake.phone_number(),
        #         "ContactMobileNumber": self.fake.cellphone_number(),
        #         "EmailAddress": self.fake.free_email(),
        #         "GpSurgeryDetails": "Test",
        #         "NumberOfChildrenUnder18": "0",
        #         "ConsentToShare": False,
        #         "DateTimeRecorded": datetime.datetime.utcnow().isoformat(),
        #         "RecordStatus": "MASTER",
        #         "InitialCallbackCompleted": None,
        #         "CallbackRequired": True,
        #         "CaseNotes": None,
        #         "AdviceNotes": None,
        #         "HelpNeeded": "Contact Tracing"
        #     }
        # ]

        # response = self.create_help_request.execute(help_requests=help_request)
        return responses
