from lib_src.lib.usecase.process_multiple_sheets import ProcessMultipleSheets
from lib_src.tests.fakes.fake_google_drive_gateway import FakeGoogleDriveGateway
from lib_src.tests.fakes.fake_pygsheet_gateway import FakePygsheetGateway
from faker import Faker
import datetime as dt

SOME_DATA = {
    'some': ['data']
}


class FakeDataProcessor:
    def execute(self, data):
        True


class TestProcessFirstSheets:
    def setup(self):
        fake = Faker()
        self.inbound_folder_id = 'inbound_folder_id'
        self.outbound_folder_id = 'outbound_folder_id'

        self.inbound_file_name = fake.file_name(extension='xlsx')
        self.inbound_file_id = fake.numerify()
        return_inbound_files = [
            {'name': self.inbound_file_name, 'id': self.inbound_file_id},
        ]
        self.fake_google_drive_gateway = FakeGoogleDriveGateway(
            return_inbound_files=return_inbound_files)
        self.fake_pygsheet_gateway = FakePygsheetGateway(SOME_DATA)
        self.data_processor = FakeDataProcessor()

        self.process_multiple_sheets = ProcessMultipleSheets(
            self.fake_google_drive_gateway, self.fake_pygsheet_gateway
        )

        self.process_multiple_sheets.execute(
            self.inbound_folder_id,
            self.outbound_folder_id,
            self.data_processor
        )

    def test_both_folders_are_searched(self):
        assert self.fake_google_drive_gateway.get_list_of_files_called_with == [
            self.inbound_folder_id, self.outbound_folder_id]

    def test_data_is_fetched(self):
        assert self.fake_pygsheet_gateway.get_data_frame_from_sheet_called_with == [
            [self.inbound_file_id, 'A1']]

    def test_data_output_file_is_created(self):
        output_file_name = f'PROCESSED_{self.inbound_file_name}_{dt.datetime.now().date().strftime("%Y-%m-%d")}'

        assert self.fake_google_drive_gateway.created_spreadsheets == [{
            'folder_id': self.outbound_folder_id,
            'spreadsheet_name': output_file_name
        }]

    def test_data_output_file_is_populated(self):
        assert len(
            self.fake_pygsheet_gateway.populate_spreadsheet_called_with) == 1


class TestProcessSecondSheets:
    def setup(self):
        fake = Faker()
        self.inbound_folder_id = 'inbound_folder_id'
        self.outbound_folder_id = 'outbound_folder_id'

        self.first_inbound_file_name = fake.file_name(extension='xlsx')
        self.first_inbound_file_id = fake.numerify()
        self.second_inbound_file_name = fake.file_name(extension='xlsx')
        self.second_inbound_file_id = fake.numerify()
        return_inbound_files = [
            {'name': self.first_inbound_file_name, 'id': self.first_inbound_file_id},
            {'name': self.second_inbound_file_name, 'id': self.second_inbound_file_id}
        ]

        return_outbound_files = [
            {'name': f'PROCESSED_{self.first_inbound_file_name}_{dt.datetime.now().date().strftime("%Y-%m-%d")}',
             'id': fake.numerify()},
        ]
        self.fake_google_drive_gateway = FakeGoogleDriveGateway(
            return_inbound_files=return_inbound_files,
            return_outbound_files=return_outbound_files)
        self.fake_pygsheet_gateway = FakePygsheetGateway(SOME_DATA)
        self.data_processor = FakeDataProcessor()

        self.process_multiple_sheets = ProcessMultipleSheets(
            self.fake_google_drive_gateway, self.fake_pygsheet_gateway
        )

        self.process_multiple_sheets.execute(
            self.inbound_folder_id,
            self.outbound_folder_id,
            self.data_processor
        )

    def test_both_folders_are_searched(self):
        assert self.fake_google_drive_gateway.get_list_of_files_called_with == [
            self.inbound_folder_id, self.outbound_folder_id]

    def test_data_is_fetched(self):
        assert self.fake_pygsheet_gateway.get_data_frame_from_sheet_called_with == [
            [self.second_inbound_file_id, 'A1']]

    def test_data_output_file_is_created(self):
        output_file_name = f'PROCESSED_{self.second_inbound_file_name}_{dt.datetime.now().date().strftime("%Y-%m-%d")}'

        assert self.fake_google_drive_gateway.created_spreadsheets == [{
            'folder_id': self.outbound_folder_id,
            'spreadsheet_name': output_file_name
        }]

    def test_data_output_file_is_populated(self):
        assert len(
            self.fake_pygsheet_gateway.populate_spreadsheet_called_with) == 1


class TestAllSheetsAreProcessed:
    def setup(self):
        fake = Faker()
        self.inbound_folder_id = 'inbound_folder_id'
        self.outbound_folder_id = 'outbound_folder_id'

        self.first_inbound_file_name = fake.file_name(extension='xlsx')
        self.first_inbound_file_id = fake.numerify()
        self.second_inbound_file_name = fake.file_name(extension='xlsx')
        self.second_inbound_file_id = fake.numerify()
        return_inbound_files = [
            {'name': self.first_inbound_file_name, 'id': self.first_inbound_file_id},
            {'name': self.second_inbound_file_name, 'id': self.second_inbound_file_id}
        ]

        return_outbound_files = [
            {'name': f'PROCESSED_{self.first_inbound_file_name}_{dt.datetime.now().date().strftime("%Y-%m-%d")}',
             'id': fake.numerify()},
            {'name': f'PROCESSED_{self.second_inbound_file_name}_{dt.datetime.now().date().strftime("%Y-%m-%d")}',
             'id': fake.numerify()},
        ]

        self.fake_google_drive_gateway = FakeGoogleDriveGateway(
            return_inbound_files=return_inbound_files,
            return_outbound_files=return_outbound_files)
        self.fake_pygsheet_gateway = FakePygsheetGateway(SOME_DATA)
        self.data_processor = FakeDataProcessor()

        self.process_multiple_sheets = ProcessMultipleSheets(
            self.fake_google_drive_gateway, self.fake_pygsheet_gateway
        )

        self.process_multiple_sheets.execute(
            self.inbound_folder_id,
            self.outbound_folder_id,
            self.data_processor
        )

    def test_both_folders_are_searched(self):
        assert self.fake_google_drive_gateway.get_list_of_files_called_with == [
            self.inbound_folder_id, self.outbound_folder_id]

    def test_data_is_not_fetched(self):
        assert len(
            self.fake_pygsheet_gateway.get_data_frame_from_sheet_called_with) == 0

    def test_no_data_output_file_is_created(self):

        assert len(self.fake_google_drive_gateway.created_spreadsheets) == 0

    def test_data_output_file_is_not_populated(self):
        assert len(
            self.fake_pygsheet_gateway.populate_spreadsheet_called_with) == 0


class TestProcessNoNewSheets:
    def setup(self):
        fake = Faker()
        self.inbound_folder_id = 'inbound_folder_id'
        self.outbound_folder_id = 'outbound_folder_id'

        self.fake_google_drive_gateway = FakeGoogleDriveGateway()
        self.fake_pygsheet_gateway = FakePygsheetGateway(SOME_DATA)
        self.data_processor = FakeDataProcessor()

        self.process_multiple_sheets = ProcessMultipleSheets(
            self.fake_google_drive_gateway, self.fake_pygsheet_gateway
        )

        self.process_multiple_sheets.execute(
            self.inbound_folder_id,
            self.outbound_folder_id,
            self.data_processor
        )

    def test_only_inbound_folder_is_searched(self):
        assert self.fake_google_drive_gateway.get_list_of_files_called_with == [
            self.inbound_folder_id]

    def test_data_is_not_fetched(self):
        assert len(
            self.fake_pygsheet_gateway.get_data_frame_from_sheet_called_with) == 0

    def test_no_data_output_file_is_created(self):
        assert len(self.fake_google_drive_gateway.created_spreadsheets) == 0

    def test_data_output_file_is_not_populated(self):
        assert len(
            self.fake_pygsheet_gateway.populate_spreadsheet_called_with) == 0
