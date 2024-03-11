"""_summary_
"""
import pandas as pd
import datetime

from net_worth import Database, Loan


class NetWorth():
    """ This class is intended to help measure the overall net worth of my assets
    """
    def __init__(self, db_name: str):
        # Load up database
        self.db = Database(db_name=db_name)

        # Preview Existing data
        self.loans = []
        self.assets = []
        self.investments = []
        self.savings = []

    def add_loan(self, amount, apr, start, end, name):
        # Prompt for additional loans
        new_loan = Loan(amount=amount, apr=apr, start=start, term=end, name=name)
        self.loans.append(new_loan)

    def remove_loan(self):
        # Preview loans to identify which to delete
        print("Previewing Options:")
        for i, loan in enumerate(self.loans):
            print(f"{i}) {loan.name}")

        # Identify which loan to remove
        index = int(input("Enter which loan you want to remove: "))
        assert index >= 0
        assert index < len(self.loans)

        # Remove the loan
        del self.loans[index]

        # View modified list
        # print("Viewing Results:")
        # for i, loan in enumerate(self.loans):
        #     print(f"{i}) {loan.name}")

        # Update database table

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
        savings = 0

        # Add value of all Investments
        invest = 0

        # Add value of all Assets
        assets = 0

        # Subtract value of all Loans
        loans = 0
        for loan in self.loans:
            # loans += loan.get_balance(datetime.datetime.today())
            loans += loan.get_balance(datetime.datetime(2024, 4, 5))

        total = savings + invest + assets - loans
        print(f"Total net worth: ${total}")

        return total

    def project_net(self, ) -> pd.DataFrame:
        # TODO: Loop throught each "update" function until reaching the current date
        # TODO: Each Update function should calculate interest and recurring changes
        # TODO: Call the current value function for each item
        # Generate a Dataframe of Net Worth over time
        return pd.DataFrame()

if __name__ == "__main__":
    my_networth = NetWorth("net_worth.db")

    my_networth.add_loan(
        start=datetime.datetime(2024, 4, 5),
        end=datetime.datetime(2033, 9, 5),
        amount=5677.25,
        apr=.025,
        name="Student Loan #1"
    )

    my_networth.add_loan(
        start=datetime.datetime(2024, 4, 5),
        end=datetime.datetime(2033, 9, 5),
        amount=4777.83,
        apr=.0348,
        name="Student Loan #2"
    )

    my_networth.date_net()
