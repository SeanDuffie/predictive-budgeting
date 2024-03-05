"""_summary_
"""
import pandas as pd
import sqlite3


class NetWorth():
    def __init__(self, db_file: str):
        # Load up database
        # Preview Existing data
        pass

    def add_loan(self):
        # Prompt for additional loans
        pass

    def remove_loan(self):
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
    my_networth = NetWorth("test.db")
