""" @file asset.py
    @author Sean Duffie
    @brief This file is meant to track net-worth assets that appreciate or depreciate over time
"""

class Asset:
    def __init__(self, init_value: float, expected_apr: float, term: int = None, name: str = "Asset"):
        """ Populate the initial parameters for the asset

        Args:
            init_value (float): Initial value of the asset when purchased
            expected_apr (float): Expected annual percentage rate, >1 is appreciating, <1 is depreciating
            term (int, optional): Number of months this asset is owned. Defaults to None.
            name (str, optional): User Friendly name for this asset. Defaults to "Asset".
        """
        self.name = name
        self.init_value = init_value
        self.expected_mpr = expected_apr / 12
        self.term = term

if __name__ == "__main__":
    Asset(330000, 0.08, 360, "House")
