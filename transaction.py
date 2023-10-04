"""
"""
import abc
import datetime

categories = [
    "Transfer",
    "Rent",
    "Gas",
    "Groceries",
    
]

class Transaction(abc.ABC):
    """ TODO:
    """
    category = 0

    def __init__(self, row: tuple):
        self.date = datetime.datetime.strptime(row[1], "%m/%d/%Y")
        self.amount = row[2]
        self.name = row[5]

    # def __init__(self, name: str, amnt: float, frq: int, cat: str):
    #     self.name = name
    #     self.amount = amnt
    #     self.frequency = frq
    #     self.category = cat

    #     self.cost_per_day = self.amount / self.frequency

    # def monthly(self):
    #     """ amount per month
    #     """
    #     return self.cost_per_day * 30

    # def biweekly(self):
    #     """ amount per paycheck
    #     """
    #     return self.cost_per_day * 14

    def __str__(self):
        return f"{self.date.date()}\t{self.amount} -> {self.name}"



# class Expense(Transaction):
#     """ TODO:
#     """

# class Income(Transaction):
#     """ Objectifies Income sources

#         This should 
#     """

#     def biweekly(self):
#         return super().biweekly()