class FakeAddCEVRequests:
    def __init__(self):
        self.execute_called_with = []

    def execute(self, cases):
        self.execute_called_with.append(cases)
