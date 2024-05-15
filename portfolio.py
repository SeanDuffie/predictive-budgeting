"""_summary_
"""
import datetime
import logging

import pandas as pd
from dateutil.rrule import MONTHLY, rrule

from net_worth import Asset, Database, Loan, Savings, calculate_term
import logFormat

# Initial Logger Settings
logFormat.format_logs(logger_name="Portfolio")
logger = logging.getLogger("Portfolio")


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
            working_years = 67 - age
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

    def mod_loan(self, name: str, amount: float = None, apr: float = None, start: datetime.date = None, term: int = None):
        """_summary_

        Args:
            name (str): _description_
            amount (float, optional): _description_. Defaults to None.
            apr (float, optional): _description_. Defaults to None.
            start (datetime.date, optional): _description_. Defaults to None.
            term (int, optional): _description_. Defaults to None.

        Raises:
            AssertionError: _description_
            AssertionError: _description_
        """
        if name not in self.loans.keys():
            raise AssertionError("Specified loan doesn't exist")

        if all([amount is None, apr is None, start is None, term is None]):
            raise AssertionError("All Parameters are null")

        if any([amount is not None, apr is not None, start is not None, term is not None]):
            # Make sure that each parameter has a value
            if amount is None:
                amount = self.loans[name].loan_amount
            if apr is None:
                apr = self.loans[name].mpr*12
            if start is None:
                start = self.loans[name].start_date
            if term is None:
                term = self.loans[name].term

            # Construct a new Loan object to replace the old one
            self.loans[name] = Loan(amount=amount, apr=apr, start=start, term=term)

    def remove_loan(self):
        """_summary_
        """
        # Preview loans to identify which to delete
        logger.info("Previewing Options:")
        for key, loan in self.loans.items():
            logger.info(f"{key}) {loan.get_balance()}")

        # Identify which loan to remove
        index = int(input("Enter which loan you want to remove: "))
        assert index >= 0
        assert index < len(self.loans)

        # Remove the loan
        del self.loans[index]

        # View modified list
        # logger.info("Viewing Results:")
        # for i, loan in enumerate(self.loans):
        #     logger.info(f"{i}) {loan.name}")

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

        if self.start is None or start < self.start:
            self.start = start

    def mod_asset(self, name: str, amount: float = None, apr: float = None, start: datetime.date = None):
        """_summary_

        Args:
            name (str): _description_
            amount (float, optional): _description_. Defaults to None.
            apr (float, optional): _description_. Defaults to None.
            start (datetime.date, optional): _description_. Defaults to None.

        Raises:
            AssertionError: _description_
            AssertionError: _description_
        """
        if name not in self.assets.keys():
            raise AssertionError("Specified asset doesn't exist")

        if all([amount is None, apr is None, start is None]):
            raise AssertionError("All Parameters are null")

        if any([amount is not None, apr is not None, start is not None]):
            # Make sure that each parameter has a value
            if amount is None:
                amount = self.assets[name].init_value
            if apr is None:
                apr = self.assets[name].expected_mpr*12
            if start is None:
                start = self.assets[name].history["Date"][0]

            # Construct a new Asset object to replace the old one
            self.assets[name] = Asset(init_value=amount, expected_apr=apr, start=start)

    def remove_asset(self):
        """_summary_
        """
        # Preview savings to identify which to delete
        logger.info("Previewing Options:")
        for key, asset in self.assets.items():
            logger.info(f"{key}: {asset.value}")

        # Identify which savings to remove
        index = input("Enter which savings you want to remove: ")
        assert index >= 0
        assert index < len(self.savings)

        # Remove the asset
        self.assets.pop(index)

    def add_investment(self, deposit: float, start: datetime.date, apr: float, recur: float = 0, name: str = "Investments"):
        """_summary_

        Args:
            deposit (float): _description_
            start (datetime.date): _description_
            apr (float): _description_
            recur (float, optional): _description_. Defaults to 0.
            name (str, optional): _description_. Defaults to "Investments".
        """
        # Prompt for additional investments
        new_sav = Savings(deposit=deposit, start=start, apr=apr, recur=recur)
        self.investments[name] = new_sav

        if self.start is None or start < self.start:
            self.start = start

    def mod_investment(self, name: str, deposit: float = None, start: datetime.date = None, apr: float = None, recur: float = None):
        """_summary_

        Args:
            name (str): _description_
            deposit (float, optional): _description_. Defaults to None.
            start (datetime.date, optional): _description_. Defaults to None.
            apr (float, optional): _description_. Defaults to None.
            recur (float, optional): _description_. Defaults to None.

        Raises:
            AssertionError: _description_
            AssertionError: _description_
        """
        if name not in self.investments.keys():
            raise AssertionError("Specified Investment doesn't exist")

        if all([deposit is None, apr is None, start is None]):
            raise AssertionError("All Parameters are null")

        if any([deposit is not None, apr is not None, start is not None]):
            # Make sure that each parameter has a value
            if deposit is None:
                deposit = self.investments[name].history["Balance"][0]
            if apr is None:
                apr = self.investments[name].mpr*12
            if start is None:
                start = self.investments[name].history["Date"][0]
            if recur is None:
                recur = self.investments[name].recur

            # Construct a new Investment object to replace the old one
            self.investments[name] = Savings(deposit=deposit, start=start, apr=apr, recur=recur)

    def remove_investment(self):
        """_summary_
        """
        # Preview savings to identify which to delete
        logger.info("Previewing Options:")
        for key, inv in self.investments.items():
            logger.info(f"{key}: {inv.balance}")

        # Identify which savings to remove
        index = input("Enter which investment you want to remove: ")
        assert index >= 0
        assert index < len(self.investments)

        # Remove the investment
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

        if self.start is None or start < self.start:
            self.start = start

    def mod_savings(self, name: str, deposit: float = None, start: datetime.date = None, apr: float = None, recur: float = None):
        """_summary_

        Args:
            name (str): _description_
            deposit (float, optional): _description_. Defaults to None.
            start (datetime.date, optional): _description_. Defaults to None.
            apr (float, optional): _description_. Defaults to None.
            recur (float, optional): _description_. Defaults to None.

        Raises:
            AssertionError: _description_
            AssertionError: _description_
        """
        if name not in self.savings.keys():
            raise AssertionError("Specified Investment doesn't exist")

        if all([deposit is None, apr is None, start is None]):
            raise AssertionError("All Parameters are null")

        if any([deposit is not None, apr is not None, start is not None]):
            # Make sure that each parameter has a value
            if deposit is None:
                deposit = self.savings[name].history["Balance"][0]
            if apr is None:
                apr = self.savings[name].mpr*12
            if start is None:
                start = self.savings[name].history["Date"][0]
            if recur is None:
                recur = self.savings[name].recur

            # Construct a new Savings object to replace the old one
            self.savings[name] = Savings(deposit=deposit, start=start, apr=apr, recur=recur)

    def remove_savings(self):
        """_summary_
        """
        # Preview savings to identify which to delete
        logger.info("Previewing Options:")
        for key, val in self.savings.items():
            logger.info(f"{key}: {val.balance}")

        # Identify which savings to remove
        index = input("Enter which savings you want to remove: ")
        assert index >= 0
        assert index < len(self.savings)

        # Remove the savings account
        self.savings.pop(index)

    def update_all(self, date):
        """_summary_

        TODO: I don't like this, the portfolio should have a set date for start, retirement, and expected remaining time
                And by generating it all on "update_all" it will be cumbersome to make any dynamic changes.
                Instead, it should be generated either on call or on creation/modification

        Args:
            date (_type_): _description_
        """
        for key, val in self.savings.items():
            val.update(date)

        for key, val in self.investments.items():
            val.update(date)

        for key, val in self.assets.items():
            val.update(date)

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
        logger.info(f"{len(self.savings)} Savings | {len(self.investments)} Investments | {len(self.assets)} Assets | {len(self.loans)} Loans")
        gross = self.calculate_gross(date)
        debts = self.calculate_debts(date)

        total = gross - debts

        logger.info("Total net worth: $%f ($%f - $%f)", total, gross, debts)

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

        logger.info("Debt to Income Ratio: %f", ratio)

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

    def to_html(self, name: str):
        loan_list = list(self.loans.items())
        asset_list = list(self.assets.items())
        investment_list = list(self.investments.items())
        savings_list = list(self.savings.items())

        rows = max(
            [
                len(self.loans),
                len(self.assets),
                len(self.investments),
                len(self.savings)
            ]
        )

        if rows > 0:
            html = f"<h2>Portfolio: {name}</h2>\n"
        else:
            html = ""
        for _ in range(rows):
            html += "\t<div class='row'>\n"

            html += "\t\t<div class='message column'>\n"
            if len(savings_list) > 0:
                sav_element = savings_list.pop(0)
                html += f"\t\t\t<h3>{sav_element[0]} (Savings)</h3>\n"
                # FIXME: Put the name back into the element objects!
                html += f"\t\t\t\t{sav_element[1].to_html(sav_element[0])}"
            html += "\t\t</div>\n"

            html += "\t\t<div class='message column'>\n"
            if len(investment_list) > 0:
                inv_element = investment_list.pop(0)
                html += f"\t\t\t<h3>{inv_element[0]} (Investment)</h3>\n"
                html += f"\t\t\t\t{inv_element[1].to_html(inv_element[0])}"
            html += "\t\t</div>\n"

            html += "\t\t<div class='message column'>\n"
            if len(asset_list) > 0:
                ast_element = asset_list.pop(0)
                html += f"\t\t\t<h3>{ast_element[0]} (Asset)</h3>\n"
                html += f"\t\t\t\t{ast_element[1].to_html(ast_element[0])}"
            html += "\t\t</div>\n"

            html += "\t\t<div class='message column'>\n"
            if len(loan_list) > 0:
                loan_element = loan_list.pop(0)
                html += f"\t\t\t<h3>{loan_element[0]} (Loan)</h3>\n"
                html += f"\t\t\t\t{loan_element[1].to_html(loan_element[0])}"
            html += "\t\t</div>\n"

            html += "\t</div>\n"

        return html

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

    logger.info("HYSA history:\n%s\n", portfolio.savings["American Express HYSA"].history)
    logger.info("ETRADE history:\n%s\n", portfolio.savings["Stocks"].history)
    logger.info("HTML:\n%s", portfolio.to_html("Portfolio"))
