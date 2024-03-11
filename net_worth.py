"""_summary_
"""
import datetime

import pandas as pd
from net_worth import Database, Loan, Savings, Asset


# FIXME: Rename to "Portfolio" soon
class NetWorth():
    """ This class is intended to help measure the overall net worth of my assets
    """
    def __init__(self, db_name: str):
        # Load up database
        self.db = Database(db_name=db_name)

        # Preview Existing data
        self.loans: list[Loan] = []
        self.assets: list[Asset] = []
        self.investments = []
        self.savings: list[Savings] = []

    def add_loan(self, amount: float, apr: float, start: datetime.date, end: datetime.date, name: str):
        """ Add a debt to your portfolio

        Args:
            amount (float): amount owed initially
            apr (float): interest rate on loan
            start (datetime.date): day that the loan started accruing interest
            end (datetime.date): date the loan is due to be paid off
            name (str): User friendly name for the loan
        """
        # Prompt for additional loans
        new_loan = Loan(
            amount=amount,
            apr=apr,
            start=start,
            term=end,
            name=name
        )
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

    def add_asset(self, init_value: float, start: datetime.date, apr: float, name: str):
        """ Add an Asset (such as a car or house) to your portfolio

        Args:
            init_value (float): cost paid for the asset
            start (datetime.date): date that the asset was purchased (used for projection)
            apr (float): expected appreciation (house) or depreciation (car) of the object
            name (str): User friendly name for the asset
        """
        # Prompt for additional assets
        new_asset = Asset(
            init_value=init_value,
            expected_apr=apr,
            start=start,
            name=name
        )
        self.assets.append(new_asset)

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

    def add_savings(self, deposit: float, start: datetime.date, apr: float, recur: float = 0):
        """ Add a savings account to be tracked in your portfolio

        Args:
            deposit (float): Initial ammount in account when tracking started
            start (datetime.date): date that tracking began
            apr (float): interest rate on account (mainly for HYSA)
            recur (float, optional): Recurring deposits going to the account. Defaults to 0.
        """
        # Prompt for additional Savings
        new_sav = Savings(deposit=deposit, start=start, apr=apr, recur=recur)
        self.savings.append(new_sav)

    def remove_savings(self):
        # Preview savings to identify which to delete
        print("Previewing Options:")
        for i, sav in enumerate(self.savings):
            print(f"{i}) {sav.name}")

        # Identify which savings to remove
        index = int(input("Enter which savings you want to remove: "))
        assert index >= 0
        assert index < len(self.savings)

        # Remove the loan
        del self.savings[index]

    def calculate_gross(self):
        """ Sums together the values of all portfolio

        TODO: integrate timeline, take date as parameter

        Returns:
            float: Sum of all components of portfolio
        """
        # Add value of all Savings
        savings = 0
        for sav in self.savings:
            savings += sav.balance

        # Add value of all Investments
        invest = 0
        for inv in self.investments:
            savings += inv.balance

        # Add value of all Assets
        assets = 0
        for ast in self.assets:
            assets += ast.value

        gross = savings + invest + assets

        return gross

    def calculate_debts(self):
        """ Sum together the current value of all debts

        TODO: integrate timeline, take date as parameter

        Returns:
            float: Sum of all loans/debts (TODO: at a given time)
        """
        # Subtract value of all Loans
        loans = 0
        for loan in self.loans:
            # loans += loan.get_balance(datetime.date.today())
            loans += loan.get_balance(datetime.date(2024, 4, 5))

        return loans

    def calculate_net(self):
        """ Calculate the net worth

        Returns:
            float: Net Worth
        """
        print(f"{len(self.savings)} Savings | {len(self.investments)} Investments | {len(self.assets)} Assets | {len(self.loans)} Loans")
        gross = self.calculate_gross()
        debts = self.calculate_debts()

        total = gross - debts

        print(f"Total net worth: ${total} (${gross} - ${debts})")

        return total

    def calculate_ratio(self):
        """ Calculate the ratio of assets compared to debts
        
        FIXME: I think I did this wrong, should it be more of a budget thing than a portfolio?

        Returns:
            float: Ratio of debts to assets. 0 is even, negative is in debt, positive is best
        """
        gross = self.calculate_gross()
        debts = self.calculate_debts()

        ratio = (gross - debts) / (gross + debts)

        # print(f"Debt to Income Ratio: {ratio}")

        return ratio

    def project_net(self, day: datetime.date) -> pd.DataFrame:
        """ Projects net worth over a period of time

        FIXME: I think this needs to be an individual function, not a dataframe
        TODO: Dataframes should be stored in each individual object, this function should just parse them

        Args:
            day (datetime.date): date of desired portfolio calculation

        Returns:
            pd.DataFrame: projection of portfolio over time TODO: replace this with a single float or a tuple
        """
        # TODO: Loop throught each "update" function until reaching the current date
        # TODO: Each Update function should calculate interest and recurring changes
        # TODO: Call the current value function for each item
        # Generate a Dataframe of Net Worth over time

        s = datetime.datetime(2024, 3, 31)
        t = datetime.timedelta(1)
        e = s + t
        print(e)

        return pd.DataFrame()

if __name__ == "__main__":
    my_networth = NetWorth("net_worth.db")

    my_networth.add_savings(
        deposit=10000,
        start=datetime.date(2024, 3, 5),
        apr=0.0435,
        recur=2000
    )

    my_networth.add_savings(
        deposit=10000,
        start=datetime.date(2024, 3, 5),
        apr=0.07,
        recur=500
    )

    my_networth.add_loan(
        start=datetime.datetime(2024, 3, 5),
        end=datetime.datetime(2033, 9, 5),
        amount=5677.25,
        apr=.025,
        name="Student Loan #1"
    )

    my_networth.add_loan(
        start=datetime.datetime(2024, 3, 5),
        end=datetime.datetime(2033, 9, 5),
        amount=4777.83,
        apr=.0348,
        name="Student Loan #2"
    )

    my_networth.calculate_net()
    # my_networth.calculate_ratio()

    # Home cost is an Asset
    home_val = 330000
    purchase_date = datetime.date(2024, 3, 1)
    my_networth.add_asset(
        init_value=home_val,
        start=purchase_date,
        apr=0.08,
        name="House"
    )

    # Down payment is subtracted from savings
    down_payment = home_val * 0.2
    my_networth.savings[0].modify_balance(-down_payment, purchase_date, "Placed down payment on house")

    # Mortgage is home cost minus down payment
    mort = home_val - down_payment
    mort_date = purchase_date + datetime.timedelta(3650)
    mort_term = 120
    my_networth.add_loan(
        start=purchase_date,
        end=mort_term,
        amount=mort,
        apr=.06,
        name="Mortgage"
    )

    my_networth.calculate_net()
    my_networth.calculate_ratio()
