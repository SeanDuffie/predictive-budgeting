"""_summary_
"""
import sys
import logging
import pandas
import numpy

CATS = {
    "Housing": .25,
    "Transportation": .10,
    "Food": .10,
    "Utilities": .5,
    "Insurance": .10,
    "Medical": .5,
    "Net Worth": .20,
    "Spending": .5
}

SUBCATS = {
    "Housing": {
        "Rent": 633,
        "Mortgage": 0,
        "Property Taxes": 0,
        "HOA dues": 0,
        "Maintenance": 0
    },
    "Transportation": {
        "Car payments": 0,
        "Gas": 200,
        "Maintenance": 150
    },
    "Food": {
        "Groceries": "",        # Track average spent per month
        "Dining out": 60        # Track number of times dining out
    },
    "Utilities": {
        "Water": 40,
        "Electricity": 80,
        "Sewer": 5,
        "Gas": 0,
        "Internet": 20,
    },
    "Medical": {                # Covered pre-tax in HSA
        "Out-of-pocket primary care": 0,
        "Specialty Care": 0,
        "Dental Care": 0,
        "Urgent Care": 0,
        "Eye Care": 15
    },
    "Net Worth": {
        "Savings": 500,
        "Investing": 250,
        "Debt": 250,            # Include amortization to mark when paid off
    },
    "Subscriptions": {
        "Spotify": 18,
        "Adobe Creative": 21,
        "OneDrive": 10,
        "Game Pass": 15,
        "Golds Gym": 37.5,
    }
}

# TODO: pull taxes from database based on location input
TAXES = {
    "Federal Income": 0.22,         #44-95, 0.24 for 95-182
    "State Income": 0,              # 0 Texas
}

class budget():
    """_summary_
    """
    def __init__(self, income: float = 62000, rent: int = 633):
        self.income = income
        self.rent = rent
        self.rent_per = self.rent / self.income
        print()

if __name__ == "__main__":
    bgt = budget()
    sys.exit(0)
