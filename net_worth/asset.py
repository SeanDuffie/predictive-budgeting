""" @file asset.py
    @author Sean Duffie
    @brief This file is meant to track net-worth assets that appreciate or depreciate over time
"""
import datetime

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

        self.history = [(self.value, init_value, start, "Started tracking asset")]
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
            self.history.append((self.value, interest, self.last_update, "Preciation Applied"))

            self.last_update += self.interval

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
        self.history.append((self.value, amount, day, note))
        
    def get_value(self, day: datetime.date):
        # if day < self.history["Date"].get(0):
        if day < self.history[0][2]:
            return 0
        else:
            return self.value

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
