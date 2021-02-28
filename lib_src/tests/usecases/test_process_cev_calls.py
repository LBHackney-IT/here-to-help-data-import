from lib_src.lib.usecase.process_cev_calls import ProcessCevCalls
from lib_src.tests.fakes.fake_add_cev_requests import FakeAddCEVRequests
import pandas as pd

NSSS = {
    'ID': ['123123'],
    'nhs_number': ['1234567890'],
    'first_name': ['Fred'],
    'last_name': ['Flintstone'],
    'date_of_birth': ['02/02/1963'],
    'address_line1': ['45 Cave Stone Road'],
    'address_line2': [''],
    'address_town_city': ['Bedrock'],
    'address_postcode': ['BR2 9FF'],
    'address_uprn': [''],
    'contact_number_calls': ['07344211233'],
    'contact_number_texts': ['02344211233'],
    'contact_email': ['fred@rocks.st'],
    'submission_datetime': ['27/01/2021 14:14:56'],
    'do_you_want_supermarket_deliveries': ['yes'],
    'do_you_need_someone_to_contact_you_about_local_support': ['yes']
}


# 'ID',
# 'middle_name',
# 'uid_submission',
# 'submission_datetime',
# 'are_you_applying_on_behalf_of_someone_else',
# 'have_you_received_an_nhs_letter',
# 'do_you_have_one_of_the_listed_medical_conditions',
# 'do_you_have_someone_to_go_shopping_for_you',
# 'ladcode',
# 'active_status',
# 'spl_category',
# 'spl_address_line1',
# 'spl_address_line2',
# 'spl_address_line3',
# 'spl_address_line4',
# 'spl_address_line5',
# 'spl_address_postcode',
# 'spl_address_uprn',
# 'help_request_id'

def test_processing_new_nsss_spreadsheet():
    fake_add_cev_requests = FakeAddCEVRequests()

    use_case = ProcessCevCalls(
        fake_add_cev_requests)

    use_case.execute(pd.DataFrame(data=[NSSS]))

    assert len(fake_add_cev_requests.execute_called_with) == 1
