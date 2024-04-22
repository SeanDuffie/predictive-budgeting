"""_summary_
"""
import datetime
import logging

import pandas as pd
from dateutil.rrule import MONTHLY, rrule

from net_worth import Asset, Database, Loan, Savings, calculate_term

# Initial Logger Settings
FMT_MAIN = "%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s"
logging.basicConfig(format=FMT_MAIN, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("Main.Main")


class Portfolio():
    """ This class is intended to help measure the overall net worth of my assets
    """
    def __init__(self, db_name: str, start: datetime.date = None, end: datetime.date = None, age: int = 23):
        # Load up database
        # self.db = Database(db_name=db_name)

        # Preview Existing data
        self.loans: dict[str, Loan] = {}
        self.assets: dict[str, Asset] = {}
        self.investments: dict[str, Savings] = {}
        self.savings: dict[str, Savings] = {}

        if start is None:
            start = datetime.date.today()
        if end is None:
            working_years = (67 - age)
            end = datetime.date(year=start.year + working_years, month=1, day=1)

        self.start = start
        self.end = end

    def add_loan(self, amount: float, apr: float, start: datetime.date, term: int, name: str):
        """ Add a debt to your portfolio

        Args:
            amount (float): amount owed initially
            apr (float): interest rate on loan
            start (datetime.date): day that the loan started accruing interest
            term (int): time in months before the loan should be paid off
            name (str): User friendly name for the loan
        """
        # Prompt for additional loans
        new_loan = Loan(
            amount=amount,
            apr=apr,
            start=start,
            term=term
        )
        self.loans[name] = new_loan

        if start < self.start:
            self.start = start

        end = start + datetime.timedelta(days=term*30)
        if end > self.end:
            self.end = end

    def remove_loan(self):
        # Preview loans to identify which to delete
        print("Previewing Options:")
        for key, loan in self.loans.items():
            print(f"{key}) {loan.get_balance()}")

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
            start=start
        )
        self.assets[name] = new_asset

        if self.start == None or start < self.start:
            self.start = start

    def remove_asset(self):
        # Preview savings to identify which to delete
        print("Previewing Options:")
        for key, asset in self.assets.items():
            print(f"{key}: {asset.value}")

        # Identify which savings to remove
        index = input("Enter which savings you want to remove: ")
        assert index >= 0
        assert index < len(self.savings)

        # Remove the loan
        self.assets.pop(index)

    def add_investment(self, deposit: float, start: datetime.date, apr: float, recur: float = 0, name: str = "Investments"):
        # Prompt for additional investments
        new_sav = Savings(deposit=deposit, start=start, apr=apr, recur=recur)
        self.investments[name] = new_sav

        if self.start == None or start < self.start:
            self.start = start

    def remove_investment(self):
        # Preview savings to identify which to delete
        print("Previewing Options:")
        for key, inv in self.investments.items():
            print(f"{key}: {inv.balance}")

        # Identify which savings to remove
        index = input("Enter which investment you want to remove: ")
        assert index >= 0
        assert index < len(self.investments)

        # Remove the loan
        self.investments.pop(index)

    def add_savings(self, deposit: float, start: datetime.date, apr: float, recur: float = 0, name: str = "Savings"):
        """ Add a savings account to be tracked in your portfolio

        Args:
            deposit (float): Initial ammount in account when tracking started
            start (datetime.date): date that tracking began
            apr (float): interest rate on account (mainly for HYSA)
            recur (float, optional): Recurring deposits going to the account. Defaults to 0.
            name (str, optional): Name to store in the savings dictionary. Defaults to "Savings".
        """
        # Prompt for additional Savings
        new_sav = Savings(deposit=deposit, start=start, apr=apr, recur=recur)
        self.savings[name] = new_sav

        if self.start == None or start < self.start:
            self.start = start

    def remove_savings(self):
        # Preview savings to identify which to delete
        print("Previewing Options:")
        for key, val in self.savings.items():
            print(f"{key}: {val.balance}")

        # Identify which savings to remove
        index = input("Enter which savings you want to remove: ")
        assert index >= 0
        assert index < len(self.savings)

        # Remove the loan
        self.savings.pop(index)

    def update_all(self, date):
        # print("Updating Savings")
        for key, val in self.savings.items():
            val.update(date)
            # print(f"\t{key}: {val.balance}")

        # print("Updating Investments")
        for key, val in self.investments.items():
            val.update(date)
            # print(f"\t{key}: {val.value}")

        # print("Updating Assets")
        for key, val in self.assets.items():
            val.update(date)
            # print(f"\t{key}: {val.value}")

    def calculate_gross(self, date: datetime.date):
        """ Sums together the values of all portfolio

        TODO: integrate timeline, take date as parameter

        Returns:
            float: Sum of all components of portfolio
        """
        # Add value of all Savings
        savings = 0
        for sav in self.savings.values():
            savings += sav.get_balance(date)

        # Add value of all Investments
        invest = 0
        for inv in self.investments.values():
            savings += inv.get_balance(date)

        # Add value of all Assets
        assets = 0
        for ast in self.assets.values():
            assets += ast.get_value(date)

        gross = savings + invest + assets

        return gross

    def calculate_debts(self, date: datetime.date):
        """ Sum together the current value of all debts

        TODO: integrate timeline, take date as parameter

        Returns:
            float: Sum of all loans/debts (TODO: at a given time)
        """
        # Subtract value of all Loans
        loans = 0
        for loan in self.loans.values():
            # loans += loan.get_balance(datetime.date.today())
            loans += loan.get_balance(date)

        return loans

    def calculate_net(self, date: datetime.date):
        """ Calculate the net worth

        Returns:
            float: Net Worth
        """
        print(f"{len(self.savings)} Savings | {len(self.investments)} Investments | {len(self.assets)} Assets | {len(self.loans)} Loans")
        gross = self.calculate_gross(date)
        debts = self.calculate_debts(date)

        total = gross - debts

        print(f"Total net worth: ${total} (${gross} - ${debts})")

        return total

    def calculate_ratio(self, date: datetime.date):
        """ Calculate the ratio of assets compared to debts

        FIXME: I think I did this wrong, should it be more of a budget thing than a portfolio?

        Returns:
            float: Ratio of debts to assets. 0 is even, negative is in debt, positive is best
        """
        gross = self.calculate_gross(date)
        debts = self.calculate_debts(date)

        try:
            ratio = (gross - debts) / (gross + debts)
        except ZeroDivisionError:
            ratio = 0

        print(f"Debt to Income Ratio: {ratio}")

        return ratio

    def project_net(self, date: datetime.date) -> pd.DataFrame:
        """ Projects net worth over a period of time

        FIXME: I think this needs to be an individual function, not a dataframe
        TODO: Dataframes should be stored in each individual object, this function should just parse them

        Args:
            day (datetime.date): date of desired portfolio calculation

        Returns:
            pd.DataFrame: projection of portfolio over time TODO: replace this with a single float or a tuple
        """
        # Keep track of all events in the plan, this will be used for any plots 
        timeline = pd.DataFrame(
            columns=[
                "Date",
                "Net",
                "Gross",
                "Debt",
                "Savings",
                "Investments",
                "Assets"
            ]
        )

        # Loop throught each "update" function until reaching the current date
        schedule = rrule(freq=MONTHLY, count=calculate_term(self.start, self.end), dtstart=self.start)
        self.update_all(date)

        # Generate a Dataframe of Net Worth over time
        for cycle in schedule:
            if cycle.date() < date:
                gross = 0
                debt = 0
                savings = 0
                invest = 0
                assets = 0
                for sav in self.savings.values():
                    cur_sav = sav.get_balance(cycle)
                    gross += cur_sav
                    savings += cur_sav
                for inv in self.investments.values():
                    cur_inv = inv.get_balance(cycle)
                    gross += cur_inv
                    invest += cur_inv
                for ast in self.assets.values():
                    cur_ast = ast.get_value(cycle)
                    gross += cur_ast
                    assets += cur_ast
                for dbt in self.loans.values():
                    debt += dbt.get_balance(cycle)

                # Append changes to timeline
                timeline.loc[len(timeline)] = [
                    cycle,
                    gross-debt,
                    gross,
                    debt,
                    savings,
                    invest,
                    assets
                ]

        timeline["Date"] = pd.to_datetime(timeline["Date"])
        # timeline.to_csv(path_or_buf="./timeline.csv")
        return timeline

    def to_html(self):
        return "<p>Testing Portfolio to HTML</p>"

if __name__ == "__main__":
    portfolio = Portfolio("net_worth.db")

    # American Express HYSA
    portfolio.add_savings(
        deposit=10000,
        start=datetime.date(2024, 3, 5),
        apr=0.0435,
        recur=2000,
        name="American Express HYSA"
    )

    # Stock Portfolio
    portfolio.add_savings(
        deposit=10000,
        start=datetime.date(2024, 3, 5),
        apr=0.07,
        recur=500,
        name="Stocks"
    )

    # Student Loans 1
    portfolio.add_loan(
        start=datetime.date(2024, 3, 5),
        term=108,
        amount=5677.25,
        apr=.025,
        name="Student Loan #1"
    )

    portfolio.add_loan(
        start=datetime.date(2024, 3, 5),
        term=108,
        amount=4777.83,
        apr=.0348,
        name="Student Loan #2"
    )

    TL2 = datetime.date(2025, 1, 1)
    portfolio.update_all(TL2)
    portfolio.calculate_net(TL2)
    portfolio.calculate_ratio(TL2)

    # Home cost is an Asset
    HOME_VAL = 330000
    PURCHASE_DATE = datetime.date(2025, 1, 1)
    portfolio.add_asset(
        init_value=HOME_VAL,
        start=PURCHASE_DATE,
        apr=0.08,
        name="House"
    )

    # Down payment is subtracted from savings
    DOWN_PAYMENT = HOME_VAL * 0.1
    portfolio.savings["American Express HYSA"].modify_balance(-DOWN_PAYMENT, PURCHASE_DATE, "Placed down payment on house")

    # Mortgage is home cost minus down payment
    MORT = HOME_VAL - DOWN_PAYMENT
    MORT_DATE = PURCHASE_DATE + datetime.timedelta(3650)
    MORT_TERM = 120
    portfolio.add_loan(
        start=PURCHASE_DATE,
        term=MORT_TERM,
        amount=MORT,
        apr=.06,
        name="Mortgage"
    )

    TL3 = datetime.date(2026, 1, 1)
    portfolio.update_all(TL3)
    portfolio.calculate_net(TL3)
    portfolio.calculate_ratio(TL3)

    print("\nHYSA history:")
    for event in portfolio.savings["American Express HYSA"].history:
        print(f"\t{event}")

    print("\nETRADE history:")
    for event in portfolio.savings["Stocks"].history:
        print(f"\t{event}")
