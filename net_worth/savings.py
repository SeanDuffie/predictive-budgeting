"""_summary_
"""
import datetime


class Savings:
    """_summary_
    """
    def __init__(self, deposit: float, start: datetime.datetime, apr: float):
        self.balance = deposit
        self.history = [(deposit, start)]
        self.apr = apr

        self.last_update = start

    def update(self):
        pass

    def update_recurring(self, amount, interval, start):
        pass

    def modify_balance(self, amount, ):
        pass

if __name__ == "__main__":
    Savings(10000, datetime.date.today())
