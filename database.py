""" responsible for loading from and saving to csv files

Features:
- Spending patterns
    - Recurring Fees
    - Statistics
        - Groceries
        - Gas
        - Utilities
- Income Tracking
- Long Term Projections

TODO: https://github.com/googlemaps/google-maps-services-python

References:
- https://www.elements.org/personal/online-banking/budgeting-tools/
- https://mint.intuit.com/

"""
# import sqlite3
import logging
import os
import sys
from datetime import datetime
from tkinter import filedialog

import numpy as np
import pandas

from transaction import Transaction  # , Expense, Income

RTDIR = os.getcwd()

class Database:
    """ Objectified database for budget organization
    """
    def __init__(self, path: str = ""):
        # Initial Logger Settings
        fmt_main = "%(asctime)s\t| %(levelname)s\t| %(message)s"
        logging.basicConfig(format=fmt_main, level=logging.INFO,
                    datefmt="%Y-%m-%d %H:%M:%S")

        # Validate the path
        if path == "" or not os.path.exists(path):
            path = filedialog.askopenfilename(
                title="Select Database File",
                filetypes=[
                    ("CSV Reports", "csv"),
                    ("JSON DB", "json")
                ],
                initialdir=f"{RTDIR}\\database\\")
            if path == "":
                logging.error("Path blank. Exiting...")
                sys.exit(1)

        # Read in the data
        self.d_frame = pandas.read_csv(path)

        # Remove the dollar sign from Amount so it can be a float
        def rem_sign(string: str):
            amnt = float(string.replace("$", "").replace(",",""))
            return amnt
        self.d_frame["Amount"] = self.d_frame["Amount"].apply(rem_sign)

    def unique(self, column: str):
        """ Returns a list of unique elements from the specified column in the dataframe

        Args:
            column (str): Name/Key of the column to be analyzed

        Returns:
            list: A list of unique values contained within the column
        """

        return list(dict.fromkeys(self.d_frame[column]))

    def sum_cats(self):
        """ Add together the sum of each category
        
        TODO: Documentation
        TODO: Add timeframe options

        Returns:
            - list: list of parent categories
            - list: list of child categories
            - NDArray: list of costs associated with each category
        """
        mas_group = self.d_frame.groupby("Master Category", observed=True)
        sum_cost = mas_group["Amount"].sum().values

        sub_group = self.d_frame.groupby(["Master Category","Subcategory"], observed=True)
        sum_cost = np.concatenate((sum_cost, sub_group["Amount"].sum().values))

        mas_list = []
        sub_list = []

        # Append initial blanks to parent and masters to children
        unique_mas = self.unique("Master Category")
        mas_list = ['']*len(unique_mas)
        sub_list.extend(unique_mas)

        # Append corresponding parents to like indices in children
        for mas, sub in sub_group["Master Category"].indices.keys():
            mas_list.append(mas)
            sub_list.append(sub)

        return mas_list, sub_list, sum_cost

    def load_save(self):
        pass

    def add_entry(self):
        pass

    def getDF(self):
        return self.d_frame

    def showDF(self):
        for row in self.d_frame.itertuples():
            print(Transaction(row))

class AmexReport:
    """ Object made to aid in reading in reports from American Express cards
    
    To Download your Report:
    1. Go to https://global.americanexpress.com/dashboard and log in to your account.
    2. Navigate to the "Statements & Activity" tab.
    3. Select the "Download Your Options" icon in the "Recent Transactions" section.
    4. Select "CSV", and check the box for "Including additional details", then download.
    5. This file can be placed anywhere and selected with a tkinter filedialog, but I
    recommend placing it in the "./database" directory TODO: adjust location for raw files later
    """
    def __init__(self, path: str = "") -> None:
        # Initial Logger Settings
        fmt_main = "%(asctime)s\t| %(levelname)s\t| %(message)s"
        logging.basicConfig(format=fmt_main, level=logging.INFO,
                    datefmt="%Y-%m-%d %H:%M:%S")

        # Validate Path
        if path == "" or not os.path.exists(path):
            path = filedialog.askopenfilename(
                title="Select American Express Report",
                filetypes=[
                    ("CSV Reports", "csv")
                ],
                initialdir=f"{RTDIR}\\database\\")

            if path == "":
                logging.error("Path blank. Exiting...")
                sys.exit(1)

        # Read in the data
        self.d_frame = pandas.read_csv(path)

        self.categorize()
        
    def categorize(self) -> list[Transaction]:
        new_entries = []
        
        cats = pandas.read_json("./database/wf_sorting.json")
        print(f"{cats=}")
        
        #TODO: Maybe have a separate lambda function for both major categories and subcategories?
        mcats = ["Housing", "Transportation", "Food", "Utilities", "Medical", "Insurance", "Net Worth", "Subscriptions", "Misc"]
        
        print(f"{cats['Transportation'].str.split().str[-1]=}")
        
        pat =  '('+'|'.join(cats.str.split().str[-1])+')'
        "()"
        self.d_frame['NCat'] = ('contains ' + self.d_frame['Description'].str.extract(pat)).fillna('other')
        print(self.d_frame["NCat"])

        # for (_, master, subcat, date, location, vendor, desc, method, amnt) in self.d_frame.iterrows():
        #     tran = Transaction(date, amnt, desc)
        #     tran.add_details(desc=desc, vendor=vendor, loc=location)

        #     # TODO: Instead of measuring based on only master and sub from WF, add description to a list of 
        #     if master == "Auto/Transportation":
        #         if subcat == "Gasoline":
        #             tran.assign_category("Transportation", "Gas")
        #         if subcat == "Maintenance/Repair":
        #             tran.assign_category("Transportation", "Maintenance")
        #         if subcat == "Parking/Tolls":
        #             tran.assign_category("Transportation", "Parking/Tolls")
        #         else:
        #             logging.warning("Unrecognized Subcategory. Enter Manually:")
        #             logging.warning("Master: %s |\tSub: %s |\tDescription: %s", master, subcat, desc)
        #             new_master = str(input("Enter manual Master Category: "))
        #             new_sub = str(input("Enter manual Subcategory: "))
        #             tran.assign_category(new_master, new_sub)

        #     if master == "Bills/Utilities":
        #         # TODO: Objectify this for more information
        #         if subcat == "Gas/Electric":
        #             tran.assign_category("Utilities", "Electricity")
        #         if subcat == "Phone/Internet":
        #             tran.assign_category("Utilities", "Internet")
        #         if subcat == "Cable/Satellite TV":
        #             tran.assign_category("Utilities", "Internet")
        #         else:
        #             logging.warning("Unrecognized Subcategory. Enter Manually:")
        #             logging.warning("Master: %s |\tSub: %s |\tDescription: %s", master, subcat, desc)
        #             new_master = str(input("Enter manual Master Category: "))
        #             new_sub = str(input("Enter manual Subcategory: "))
        #             tran.assign_category(new_master, new_sub)

        #     if master == "Business/Office":
        #         if subcat == "Postage/Shipping":
        #             tran.assign_category("Misc", "Postage")
        #         if subcat == "Maintenance/Repair":
        #             tran.assign_category("Transportation", "Maintenance")
        #         if subcat == "Parking/Tolls":
        #             tran.assign_category("Transportation", "Parking/Tolls")
        #         else:
        #             logging.warning("Unrecognized Subcategory. Enter Manually:")
        #             logging.warning("Master: %s |\tSub: %s |\tDescription: %s", master, subcat, desc)
        #             new_master = str(input("Enter manual Master Category: "))
        #             new_sub = str(input("Enter manual Subcategory: "))
        #             tran.assign_category(new_master, new_sub)
                    
                    
        #     if master == "Auto/Transportation":
        #         if subcat == "Gasoline":
        #             tran.assign_category("Transportation", "Gas")
        #         if subcat == "Maintenance/Repair":
        #             tran.assign_category("Transportation", "Maintenance")
        #         if subcat == "Parking/Tolls":
        #             tran.assign_category("Transportation", "Parking/Tolls")
        #         else:
        #             logging.warning("Unrecognized Subcategory. Enter Manually:")
        #             logging.warning("Master: %s |\tSub: %s |\tDescription: %s", master, subcat, desc)
        #             new_master = str(input("Enter manual Master Category: "))
        #             new_sub = str(input("Enter manual Subcategory: "))
        #             tran.assign_category(new_master, new_sub)
        #     else:
        #         logging.warning("Unrecognized Master Category. Enter Manually:")
        #         logging.warning("Master: %s |\tSub: %s |\tDescription: %s", master, subcat, desc)
        #         new_master = str(input("Enter manual Master Category: "))
        #         new_sub = str(input("Enter manual Subcategory: "))
        #         tran.assign_category(new_master, new_sub)

        #     new_entries.append(tran)

        return new_entries

class WFReport:
    """ Object made to aid in reading in reports from American Express cards
    
    To Download your Report:
    1. Go to https://connect.secure.wellsfargo.com/accounts/start and log in to your account.
    2. Mouse over the "Plan & Learn" option on the Nav bar.
    3. Select the "View Spending Report" option in the "Budget & Save" section.
    4. Scroll down and select the "Download in Excel option for "Past 18 months"
    5. This file can be placed anywhere and selected with a tkinter filedialog, but I
    recommend placing it in the "./database" directory TODO: adjust location for raw files later
    """
    def __init__(self, path: str = "") -> None:
        # Initial Logger Settings
        fmt_main = "%(asctime)s\t| %(levelname)s\t| %(message)s"
        logging.basicConfig(format=fmt_main, level=logging.INFO,
                    datefmt="%Y-%m-%d %H:%M:%S")

        # Validate Path
        if path == "" or not os.path.exists(path):
            path = filedialog.askopenfilename(
                title="Select Wells Fargo Report",
                filetypes=[
                    ("CSV Reports", "csv")
                ],
                initialdir=f"{RTDIR}\\database\\")

            if path == "":
                logging.error("Path blank. Exiting...")
                sys.exit(1)

        # Read in the data
        self.d_frame = pandas.read_csv(path)

        def rem_sign(string: str):
            """ Remove the dollar sign from Amount so it can be a float

            Args:
                string (str): the current string that's being modified

            Returns:
                str: the modified string, can be .apply()'d on a dataframe column
            """
            amnt = float(string.replace("$", "").replace(",",""))
            return amnt
        self.d_frame["Amount"] = self.d_frame["Amount"].apply(rem_sign)


    def num_major_cats(self):
        unique_cats = list(dict.fromkeys(self.d_frame["Master Category"]))
        print(type(self.d_frame["Master Category"]))
        print("Major Categories")
        print(unique_cats)
        num = len(unique_cats)
        return num

    def num_sub_cats(self):
        unique_cats = list(dict.fromkeys(self.d_frame["Subcategory"]))
        print("Subcategories:")
        print(unique_cats)
        num = len(unique_cats)
        return num

class Address:
    street = ""
    city = ""
    state = ""
    zip = ""
    country = "UNITED STATES"
    def __init__(self, street="", city="", state="", zip=""):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        
    def geolocate(self):
        """_summary_
        """
        address = self.format_address(zip_flag=False)
        # coords = gmaps.geocode(address)
        # return coords
        return (0,0)
    
    def coords_to_address(self):
        # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
        return '1600 Amphitheatre Parkway, Mountain View, CA'
    
    def format_address(self, zip_flag=True):
        """_summary_

        Args:
            zip_flag (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        fmt = f"{self.street}, {self.city}, {self.state}"
        if zip_flag:
            fmt += f" {self.zip}"
        return fmt

if __name__ == "__main__":
    # db = Database()
    # db.sum_cats()
    # df = db.getDF()

    am = AmexReport("./database/reports/AmEx_activity_2.csv")

    # categories = pandas.DataFrame({"category": ["wire", "energy", "loans", "advisors"]})
    # domains = pandas.DataFrame({"Sno": list(range(1, 10)),
    #                 "Domain_IDs": [
    #                     "herowire.com",
    #                     "xyzenergy.com",
    #                     "financial.com",
    #                     "oo-loans.com",
    #                     "okwire.com",
    #                     "cleanenergy.com",
    #                     "pop-advisors.com",
    #                     "energy-advisors.com",
    #                     "wire-loans.com"]})

    # categories["common"] = 0
    # domains["common"] = 0

    # possibilities = pandas.merge(categories, domains, how="outer")
    # possibilities["satisfied"] = possibilities.apply(lambda row: row["category"] in row["Domain_IDs"], axis=1)
    
    
    
