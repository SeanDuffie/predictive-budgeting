""" @file budget.py
    @author Sean Duffie
    @brief Based on the user's yearly income, it calculates the portions to various expenses and savings
    
    TODO: 
    FIXME: The budget should be calculated on a monthly basis, this would solve the problems of paying of the loans or filling the emergency fund
"""
from .income import Income

distribution = {
    "Donations": 50,
    "Insurance": 0,
    "Housing": 1450,
    "Utilities": 200,
    "Internet": 90,
    "Transportation": 80,
    "Food": 250,
    "Debts (minimum)": 0,
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
        self.net = self.income.net_monthly
        self.remaining = self.net

        self.distribution = self.generate_budget()

    def add_minimum_payments(self, min_payment: float):
        distribution["Debts (minimum)"] += min_payment

    def generate_budget(self):
        return distribution

    def apply_budget(self, budget_dict: dict):
        remaining = self.income.gross_monthly
        ### Pre Tax ###
        # TODO: (FOO1) Subtract Deductibles from gross
        donations = budget_dict["Donations"]
        budget_dict.pop("Donations")
        self.income.add_deductible(donations)
        remaining -= donations

        insurance = budget_dict["Insurance"]
        budget_dict.pop("Insurance")
        self.income.add_deductible(insurance)
        remaining -= insurance

        # splittable = 1990
        # splittable_term = splittable * 14 = 27860
        # divided = (splittable / 2) * 3 = 3501
        # spread_diff = (splittable_term - divided) / 14 250
        # new_rent = rent - spread_diff = 1450

        # TODO: (FOO2) Subtract Employer 401K Match from gross

        # Calculate Tax
        taxes = self.income.taxes / 12

        # Subtract tax
        remaining -= taxes
        ### Post Tax ###
        # TODO: Subtract Living Expenses
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
    
    def gen_percents(self, budget_dict: dict):
        gross_ratios = budget_dict.copy()
        net_ratios = budget_dict.copy()

        for key, val in budget_dict.items():
            gross_ratios[key]= val / self.income.gross_monthly
            net_ratios[key] = val / self.income.net_monthly

        # if debug:
        print("\nExpense \tAmount \tGross \tNet")
        for key in budget_dict.keys():
            print(f"{key[:8].ljust(8, ' ')} \t${budget_dict[key]} \t{round(gross_ratios[key]*100, 2)}% \t{round(net_ratios[key]*100, 2)}%")


if __name__ == "__main__":
    bgt = Budget(104000, state="GA")
    bgt.apply_budget(distribution)
    bgt.gen_percents(distribution)
