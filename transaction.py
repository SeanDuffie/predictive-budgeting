"""
"""
import abc

class Transaction(abc.ABC):
    """ TODO:
    """
    name = ""
    amount = 0
    frequency = 30
    category = 0

    t_year = 0
    t_mon = 0
    t_dom = 0

    # def __init__(self, ):

    def __init__(self, name: str, amnt: float, frq: int, cat: str):
        self.name = name
        self.amount = amnt
        self.frequency = frq
        self.category = cat

        self.cost_per_day = self.amount / self.frequency

    def monthly(self):
        """ amount per month
        """
        return self.cost_per_day * 30

    def biweekly(self):
        """ amount per paycheck
        """
        return self.cost_per_day * 14

    def date(self, string: str):
        """ extract date
        """
        self.t_mon,self.t_dom,self.t_year = string.split(sep="/")
    def __str__(self):
        return f"{self.t_year}/{self.t_mon}/{self.t_dom}"



# class Expense(Transaction):
#     """ TODO:
#     """

# class Income(Transaction):
#     """ Objectifies Income sources

#         This should 
#     """

#     def biweekly(self):
#         return super().biweekly()
    