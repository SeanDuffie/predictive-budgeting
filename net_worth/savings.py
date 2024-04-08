"""_summary_
"""
import datetime

from dateutil.relativedelta import relativedelta
import pandas as pd


class Savings:
    """_summary_
    """
    def __init__(self, deposit: float, start: datetime.date, apr: float, recur: float = 0, interval: int = 1):
        self.balance = deposit
        self.recur = (recur, start, interval)
        self.mpr = apr / 12

        self.history = pd.DataFrame(
            columns = [
                "Date",
                "Balance",
                "Deposit",
                "Interest",
                "Description"
            ],
            data = [[
                start,
                self.balance,
                deposit,
                0,
                "Initial deposit"
            ]]
        )
        self.history["Date"] = pd.to_datetime(self.history["Date"])

        self.last_update = start
        self.interval = relativedelta(months=1)

    def update(self, day: datetime.date = None):
        """ Call every pay period to update all transactions

        TODO: Add a datetime and validate to prevent multiple calls
        """
        if day is None:
            day = datetime.date.today()

        while self.last_update < day:
            if self.recur is not None:
                # Apply recurring deposit
                self.balance += self.recur[0]

                # Apply Interest TODO: put this before or after deposit?
                interest = self.balance * (self.mpr)
                self.balance += interest

                # Append changes to history
                self.history.loc[len(self.history)] = [
                    self.last_update,
                    self.balance,
                    self.recur[0],
                    interest,
                    "Recurring Deposit + Interest"
                ]

            self.last_update += self.interval

        self.history["Date"] = pd.to_datetime(self.history["Date"])

    def update_recurring(self, amount: float, start: datetime.date = None, interval: int = 1):
        """ Update the recurring deposits going to this account

        Args:
            amount (float): Monthly amount going to this account. TODO: Add options for weekly paychecks
            start (datetime.date, optional): Date that this recurrance should be effective. Defaults to None.
            interval (int, optional): Interval between payments, currently unused. Defaults to 1.
        """
        if start is None:
            start = datetime.date.today()

        self.recur = (amount, start, interval)

    def modify_balance(self, amount: float, date: datetime.date = None, note: str = "Modified balance"):
        """ Use this if there are big withdrawls or deposits outside of the plan

        Args:
            amount (float): Amount to modify balance by (positive if deposit, negative if withdrawl)
            note (str): String describing reason for modification. Will be stored in history.
        """
        if date is None:
            date = datetime.date.today()

        self.balance += amount
        # Append changes to history
        self.history.loc[len(self.history)] = [
            date,
            self.balance,
            amount,
            0,
            note
        ]

    def get_balance(self, date: datetime.date):
        """ Gets the balance of the account on a given day

        Args:
            date (datetime.date): Month of the expected transaction

        Returns:
            float: Amount in the balance
        """
        date1 = datetime.datetime(date.year, date.month, 1)
        if date1.month == 12:
            date2 = datetime.datetime(date.year+1, 1, 1)
        else:
            date2 = datetime.datetime(date.year, date.month + 1, 1)
        if date1 < self.history["Date"].get(0):
            # print("Too Early")
            amount = 0
        elif date1 > self.history["Date"].get(self.history["Date"].size - 1):
            # print("Too Late")
            amount = 0
        else:
            # Find the row of the Amortization table for the requested date
            result = self.history.loc[(self.history["Date"] >= date1)
                                & (self.history["Date"] < date2)].reset_index()

            # Extract the balance amount from the table row
            amount = result["Balance"].get(0)

        # FIXME: Temporary error handling for calling a loan that hasn't been initialized yet
        if amount is None:
            print("This should never be printed")
            amount = 0

        return amount

if __name__ == "__main__":
    ACC = Savings(10000, datetime.date.today(), 0.0435)
    ACC.update_recurring(2000)

    # TODO: Sort history chronologically, maybe make into dataframe
    ACC.update(datetime.date(2026, 1, 1))

    print("Savings history:")
    for item in ACC.history:
        print(f"\t{item}")
