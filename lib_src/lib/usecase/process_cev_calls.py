from ..helpers import clean_data


class ProcessCevCalls:
    COLS = [
        'nhs_number',
        # 'ID',
        'first_name',
        # 'middle_name',
        'last_name',
        'date_of_birth',
        'address_line1',
        'address_line2',
        'address_town_city',
        'address_postcode',
        'address_uprn',
        'contact_number_calls',
        'contact_number_texts',
        'contact_email',
        # 'uid_submission',
        # 'submission_datetime',
        # 'are_you_applying_on_behalf_of_someone_else',
        # 'have_you_received_an_nhs_letter',
        'do_you_want_supermarket_deliveries',
        'do_you_need_someone_to_contact_you_about_local_support',
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
    ]

    def __init__(self, add_cev_requests):
        self.add_cev_requests = add_cev_requests

    def execute(self, data_frame):
        data_frame = clean_data(columns=self.COLS, data_frame=data_frame)

        processed_data_frame = self.add_cev_requests.execute(data_frame)

        return processed_data_frame
