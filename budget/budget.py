"""_summary_
"""
from income import Income

distribution = {
    "Donations": 50,
    "Housing": 1700,
    "Utilities": 200,
    "Internet": 90,
    "Transportation": 80,
    "Food": 250,
    "Insurance": 0,
    "Debts (minimum)": 100,
    "HYSA (Emergency)": 2500,
    "Investments": 500,
    "Debts (extra)": 0,
    "HYSA (Extra)": 0,
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

        self.distribution = self.generate_budget()

    def generate_budget(self):
        return distribution

    def apply_budget(self, budget_dict: dict):
        remaining = self.remaining
        # TODO: (FOO1) Subtract Deductibles


        # TODO: (FOO2) Subtract Employer 401K Match


        # TODO: Subtract Expenses
        for key, value in budget_dict.items():
            remaining -= value
            print(f"Spending ${value} on {key}. New balance = ${remaining}")

        # TODO: (FOO3) Subtract High-Interest Debt


        # TODO: (FOO4) If Emergency Reserves is not full, contribute
        

        # TODO: (FOO5) Max out Roth & HSA
        

        # TODO: (FOO6) Max out retirement
        

        # TODO: (FOO7) Accumulation
        # Contribute to savings
        # Contribute to investment
        

        # TODO: (FOO8) Prepaid future expenses?
        

        # TODO: (FOO9) Low interest debt (most of the time just do minimum)
        

        self.remaining = remaining
        return remaining


if __name__ == "__main__":
    bgt = Budget(104000, state="GA")
    bgt.apply_budget(distribution)
