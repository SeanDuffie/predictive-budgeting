""" @file asset.py
    @author Sean Duffie
    @brief This file is meant to track net-worth assets that appreciate or depreciate over time
"""
import datetime

class Asset:
    def __init__(self, init_value: float, expected_apr: float, start: datetime.date = None, name: str = "Asset"):
        """ Populate the initial parameters for the asset

        Args:
            init_value (float): Initial value of the asset when purchased
            expected_apr (float): Expected annual rate, >1 is appreciating, <1 is depreciating
            term (int, optional): Number of months this asset is owned. Defaults to None.
            name (str, optional): User Friendly name for this asset. Defaults to "Asset".
        """
        self.name = name
        self.init_value = init_value        # TODO: may not need this if the init value can be found in the history
        self.value = init_value
        self.expected_mpr = expected_apr / 12

        self.history = [(self.value, init_value, start, "Started tracking asset")]
        self.last_update = start

    def update(self, day: datetime.date = None):
        """ Call every pay period to update all transactions

        TODO: Add a datetime and validate to prevent multiple calls
        """
        if day is None:
            day = datetime.date.today()
        self.last_update = day

        interest = self.value * (self.expected_mpr)
        self.value += interest
        self.history.append((self.value, interest, day, "Preciation Applied"))

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

if __name__ == "__main__":
    HOUSE = Asset(330000, 0.08, 360, "House")

    HOUSE.update()
    HOUSE.update()
    HOUSE.modify_value(7000, datetime.date.today(), "Replaced Drywall")
    HOUSE.update()
    HOUSE.update()
    HOUSE.update()
    HOUSE.update()
    HOUSE.update()
    HOUSE.update()
    HOUSE.update()
    HOUSE.modify_value(-3000, datetime.date.today(), "Basement Flooded")
    HOUSE.update()
    HOUSE.update()
    HOUSE.update()

    print("House value history:")
    for item in HOUSE.history:
        print(f"\t{item}")
