import pandas as pd

class FakePygsheetGateway:
    def __init__(self, return_dataframe):
        self.return_dataframe = return_dataframe
        self.get_data_frame_from_sheet_called_with = []
        self.populate_spreadsheet_called_with = []

    def get_data_frame_from_sheet(self, spreadsheet_id, start_cell):
        self.get_data_frame_from_sheet_called_with.append(
            [spreadsheet_id, start_cell]
        )

        return pd.DataFrame(data=self.return_dataframe)

    def populate_spreadsheet(self, spreadsheet, spreadsheet_key):
        self.populate_spreadsheet_called_with.append([spreadsheet, spreadsheet_key])
