""" @file asset.py
    @author Sean Duffie
    @brief This file is meant to track net-worth assets that appreciate or depreciate over time
"""
import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta


class Asset:
    def __init__(self, init_value: float, expected_apr: float, start: datetime.date = None):
        """ Populate the initial parameters for the asset

        Args:
            init_value (float): Initial value of the asset when purchased
            expected_apr (float): Expected annual rate, >1 is appreciating, <1 is depreciating
            term (int, optional): Number of months this asset is owned. Defaults to None.
        """
        self.init_value = init_value        # TODO: may not need this if the init value can be found in the history
        self.value = init_value
        self.expected_mpr = expected_apr / 12

        self.history = pd.DataFrame(
            columns = [
                "Date",
                "Balance",
                "Change",
                "Description"
            ],
            data = [[
                start,
                self.value,
                init_value,
                "Started tracking asset"
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
            interest = self.value * (self.expected_mpr)
            self.value += interest
            self.history.loc[len(self.history)] = [
                self.last_update,
                self.value,
                interest,
                "Preciation Applied"
            ]

            self.last_update += self.interval

        self.history["Date"] = pd.to_datetime(self.history["Date"])

    def modify_value(self, amount: float, day: datetime.date = None, note: str = "Modified value"):
        """ Use this if there are changes that affect the value of the Asset
        
        Examples:
            Replaced Tires on Vehicle (value increases)
            Basement floods in House (value decreases)
            Retiled flooring in Kitchen (value increases)

        Args:
            amount (float): Amount to modify value by (positive if improvement, negative if damage)
            note (str): String describing reason for modification. Will be stored in history.
        """
        if day is None:
            day = datetime.date.today()

        self.value += amount
        self.history.loc[len(self.history)] = [
            day,
            self.value,
            amount,
            note
        ]
        self.history["Date"] = pd.to_datetime(self.history["Date"])

    def get_value(self, date: datetime.date):
        """ Gets the value on a specified date

        Args:
            date (datetime.date): Day being queried for value

        Returns:
            float: Value of asset on given day
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

    def to_html(self, name: str):
        html = f"<p>Starting Value:\t${self.history["Balance"].get(0)}</p>\n"
        html += f"<p>Expected APR:   \t{self.expected_mpr*1200}%</p>\n"
        html += f"<p>Starting Date:  \t{self.history["Date"].get(0)}</p>\n"

        return html


if __name__ == "__main__":
    purchase_date = datetime.date(2025, 1, 1)
    HOUSE = Asset(330000, 0.08, purchase_date)

    # TODO: Sort history chronologically, maybe make into dataframe
    HOUSE.modify_value(7000, datetime.date(2024, 2, 1), "Refinished Tile")
    HOUSE.modify_value(-3000, datetime.date(2024, 4, 1), "Water Damage")
    HOUSE.update(datetime.date(2026, 1, 1))

    print("House value history:")
    for item in HOUSE.history:
        print(f"\t{item}")
