"""_summary_
"""
import datetime


class Savings:
    """_summary_
    """
    def __init__(self, deposit: float, start: datetime.date, apr: float, recur: float = 0, interval: int = 1):
        self.balance = deposit
        self.recur = (recur, start, interval)
        self.mpr = apr / 12

        self.history = [(self.balance, deposit, start, "Initial deposit")]
        self.last_update = start

    def update(self, day: datetime.date = None):
        """ Call every pay period to update all transactions

        TODO: Add a datetime and validate to prevent multiple calls
        """
        if day is None:
            day = datetime.date.today()
        self.last_update = day

        if self.recur is not None:
            self.balance += self.recur[0]
            self.history.append((self.balance, self.recur[0], day, "Recurring Deposit"))

        interest = self.balance * (self.mpr)
        self.balance += interest
        self.history.append((self.balance, interest, day, "Interest Applied"))

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

    def modify_balance(self, amount: float, day: datetime.date = None, note: str = "Modified balance"):
        """ Use this if there are big withdrawls or deposits outside of the plan

        Args:
            amount (float): Amount to modify balance by (positive if deposit, negative if withdrawl)
            note (str): String describing reason for modification. Will be stored in history.
        """
        if day is None:
            day = datetime.date.today()

        self.balance += amount
        self.history.append((self.balance, amount, day, note))

if __name__ == "__main__":
    ACC = Savings(10000, datetime.date.today(), 0.0435)
    ACC.update_recurring(2000)

    ACC.update()
    ACC.update()
    ACC.update()
    ACC.update()
    ACC.update()
    ACC.update()
    ACC.update()
    ACC.update()
    ACC.update()
    ACC.update()
    ACC.update()
    ACC.update()

    print("Savings history:")
    for item in ACC.history:
        print(f"\t{item}")
