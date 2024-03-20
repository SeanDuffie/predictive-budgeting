"""_summary_
"""
from income import Income

distribution = {
    "Housing": (None, 0.2),
    "Utilities": (None, 0),
    "Internet": (90, None),
    "Transportation": 0,
    "Food": 0.03,
    "Insurance": 0,
    "Debts (minimum)": (100, 0),
    "Emergency Savings": 0,
    "Debts (extra)": 0,
    "HYSA": 0,
    "Investments": 0,
    
}


class Budget():
    """_summary_
    """
    def __init__(self, gross: float, state: str, **flags):
        # TODO: add flags for things like paycheck/bill interval
        for key, value in flags.items():
            print("{}: {}".format(key,value))

        # Collect Income and Region
        self.income = Income(gross, state)
        self.taxes = self.income.taxes / 12
        self.net = self.income.net_monthly
        self.remaining = self.net

    def generate_budget(self):
        return distribution

    def apply_budget(self, budget_dict):

        # TODO: (FOO1) Subtract Deductibles
        
        # TODO: (FOO2) Subtract Employer 401K Match
        
        # TODO: (FOO3) Subtract High-Interest Debt
        
        # TODO: Subtract Expenses
            # Rent
            # Utilities
            # Groceries
            # 
        
        # TODO: (FOO4) If Emergency Reserves is not full, contribute
        
        

if __name__ == "__main__":
    bgt = Budget(104000)
    print(bgt)
