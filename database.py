""" responsible for loading from and saving to csv files
"""
import pandas
from transaction import Transaction#, Expense, Income

class Database:
    def __init__(self):
        self.df = pandas.read_csv("./database/CreditCardRefined.csv")
    def load_save(self):
        pass

    def add_entry(self):
        pass

    def getDF(self):
        return self.df
    
    def showDF(self):
        for row in self.df.itertuples():
            print(Transaction(row))

if __name__ == "__main__":
    # first = Transaction("rent", 633.34, 1, "rent")
    # print(first)
    Database()
