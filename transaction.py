"""
"""
import abc
import datetime


class Transaction():
    """ TODO:
    """
    # Category of the transaction
    master_cat = ""
    sub_cat = ""
    
    # Duration in months of a recurring payment. 0 is not recurring. -1 is indefinite.
    duration = 0
    # Amount of months in between payments. 1 is monthly, 3 is quarterly, 12 is yearly.
    interval = 0

    # Optional additional data
    vendor = ""
    location = ""
    description = ""

    def __init__(self, date, amount, name):
        self.date = datetime.datetime.strptime(date, "%m/%d/%Y")
        self.amount = amount
        self.name = name

    def assign_category(self, master, sub):
        self.master_cat = master
        self.sub_cat = sub

    def recurring(self, interval, duration = -1):
        self.interval = interval
        self.duration = duration

    def add_details(self, desc = "", vendor = "", loc = ""):
        self.description = desc
        self.vendor = vendor
        self.location = loc

    # def to_dataframe(self):
    #     return f"{}"

    def __str__(self):
        return f"{self.date.date()}\t{self.amount} -> {self.name}"
