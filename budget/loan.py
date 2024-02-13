"""_summary_
"""

class Loan():
    def __init__(self, amount: float, apr: float):
        self.loan_amount = amount
        self.principal = amount
        self.apr = apr
        
        self.interest_table = []
        self.principal_table = []
        self.total_interest = 0

    def make_payment(self, monthly_payment):
        interest = self.principal*self.apr/12

    def minimum_payment(self, timeframe):
        pass
