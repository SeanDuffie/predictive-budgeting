"""_summary_
"""
import pandas as pd

from .net_worth import *


class NetWorth():
    """ This class is intended to help measure the overall net worth of my assets
    """
    def __init__(self, db_file: str):
        # Load up database
        self.db = Database()
        # Preview Existing data
        self.loans = []
        self.assets = []
        self.investments = []
        self.savings = []

    def add_loan(self):
        # Prompt for additional loans
        self.loans.append(Loan())

    def remove_loan(self, name: str):
        # Identify which loan to remove
        # Drop loan from database table
        pass

    def add_asset(self):
        # Prompt for additional assets
        pass

    def remove_asset(self):
        # Identify which asset to remove
        # Drop Asset from database table
        pass

    def add_investment(self):
        # Prompt for additional investments
        pass

    def remove_investment(self):
        # Identify which investment to remove
        # Drop investment from database table
        pass

    def add_savings(self):
        # Prompt for additional Savings
        pass

    def remove_savings(self):
        # Identify which investment to remove
        # Drop investment from database table
        pass

    def calculate_gross(self):
        return 0

    def calculate_debts(self):
        return 0

    def date_net(self):
        # Add value of all Savings
        # Add value of all Investments
        # Add value of all Assets
        # Subtract value of all Loans
        return 0

    def project_net(self) -> pd.DataFrame:
        # Generate a Dataframe of Net Worth over time
        return pd.DataFrame()

if __name__ == "__main__":
    my_networth = NetWorth("net_worth.db")
