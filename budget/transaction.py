""" @file transaction.py
    @author Sean Duffie
    @brief Base class of transaction, this will be inherited by others
"""
import datetime


class Transaction:
    """_summary_
    """
    def __init__(self,
                 amnt: float,
                 interval: float = 30,
                 start: datetime.datetime | None = None,
                 end: datetime.datetime | None = None):
        self.amount = amnt
        self.interval = datetime.timedelta(days=interval)
        self.date_start = start
        self.date_recent = start
        self.date_end = end

    def get_monthly(self) -> float:
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.amount/self.interval

    def next_occur(self, previous_date: datetime.datetime | None = None, current_date : datetime.datetime | None = None) -> datetime.datetime:
        """_summary_

        Args:
            previous_date (datetime | None, optional): _description_. Defaults to None.

        Returns:
            datetime: _description_
        """
        # If no "previous_date" date is supplied, then assume that time is now
        if previous_date is None:
            previous_date = self.date_recent
        next_date = previous_date

        if current_date is None:
            current_date = datetime.datetime.now()

        # Estimate the day of the next payment
        c = 0
        while next_date < current_date:
            c += 1
            next_date += self.interval
        print(f"{c-1} Payments Behind")

        print(f"Next payment due on {next_date.strftime('%Y-%m-%d')}")

        return next_date

if __name__ == "__main__":
    sub = datetime.datetime(2024, 2, 1)
    trn = Transaction(1641, interval=30, start=sub)
    trn.next_occur()

    paycheck = Transaction(1466, 7, sub)
    paycheck.next_occur()
