""" @file budget.py
    @author Sean Duffie
    @brief Based on the user's yearly income, it calculates the distributions to various sources

    TODO: objectify the distribution
    FIXME: The budget should be calculated on a monthly basis
            this would solve the problems of paying of the loans or filling the emergency fund
"""
import pandas as pd
import datetime
import dataclasses
from dateutil.rrule import MONTHLY, rrule
import logging

from .income import Income

logger = logging.getLogger("Budget")

distribution = {
    "Deduct": 50,
    "Debts (minimum)": 0,
    "Housing": 1700,
    "Utilities": 200,
    "Internet": 90,
    "Transportation": 80,
    "Food": 250,
    "Insurance": 0,
    "HYSA (Emergency)": 2500,
    "Investments": 500,
    "Debts (extra)": 0,
    "HYSA (Extra)": 0,
}


@dataclasses.dataclass
class Distribution:
    Income: float = 0
    Deduct: float = 0
    Tax: float = 0
    Debt: float = 0
    Housing: float = 0
    Utilities: float = 0
    Internet: float = 0
    Transport: float = 0
    Food: float = 0
    Savings: float = 0
    Invest: float = 0

    def to_df(self):
        elements = [Income, ]
        return elements


class Budget():
    """_summary_
    """
    plan: pd.DataFrame

    def __init__(self, gross: float, state: str, start: datetime.date, end: datetime.date, **flags):
        # TODO: add flags for things like paycheck/bill interval
        for key, value in flags.items():
            print("{}: {}".format(key,value))

        # Collect Income and Region
        self.income = Income(gross, state)
        self.net = self.income.net_monthly
        self.remaining = self.net

        dist = [
            'Date', 'Income', 'Deduct', 'Tax', 'Debt', 'Housing', 'Utilities',
            'Internet', 'Transport', 'Food', 'Savings', 'Investments'
        ]
        self.plan = pd.DataFrame(columns=dist)
        term = (end.year - start.year) * 12 + (end.month - start.month)
        for month in rrule(freq=MONTHLY, count=term, dtstart=start):
            self.plan.loc[len(self.plan)] = [month, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.plan["Date"] = pd.to_datetime(self.plan["Date"])

    def default_budget(self, dist: Distribution):
        date, elements = dist.to_df()
        self.plan

    def update_range(self, start, end, dist):
        if start > end:
            logger.error("End date must be after start date")
        if start < self.plan["Date"].get(0):
            logger.error("Start Date must be within the Budget range")
        elif start > self.plan["Date"].get(self.plan["Date"].size - 1):
            logger.error("Start Date must be within the Budget range")
        if end < self.plan["Date"].get(0):
            logger.error("End Date must be within the Budget range")
        elif end > self.plan["Date"].get(self.plan["Date"].size - 1):
            logger.error("End Date must be within the Budget range")

        term = (end.year - start.year) * 12 + (end.month - start.month)
        for month in rrule(freq=MONTHLY, count=term, dtstart=start):
            self.plan.loc[len(self.plan)] = [month, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.plan["Date"] = pd.to_datetime(self.plan["Date"])
        elements = dist.to_df()

    def get_month(self, date: datetime.date):
        return self.plan[self.plan.loc


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
