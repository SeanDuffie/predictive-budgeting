""" @file loan.py
    @author Sean Duffie
    @brief This Loan object is intended to help me organize loan-related features of my budget

    References:
    - https://www.bankrate.com/mortgages/amortization-calculator/
"""
import datetime

import pandas as pd
from dateutil.rrule import MONTHLY, rrule

from .helpers import calculate_term


class Loan():
    """ The Loan object allows me to store data related to loans without having to retype
        it every time I want to try to experiment with new parameters
    """
    def __init__(self, amount: float, apr: float, start: datetime.date = None, term: int = 120, name: str = "Loan"):
        """ Populate the inital parameters of the loan
        Args:
            amount (float): Total starting value for the loan
            apr (float): annual percentage rate
            term (int): maximum number of months for this loan to be paid off
            name (str, optional): User Friendly name for this loan. Defaults to "Loan".
        """
        self.name = name
        self.loan_amount = amount
        self.principal = amount
        self.mpr = apr / 12

        if start is None:
            self.start_date = datetime.date.today()
        else:
            self.start_date = start

        if isinstance(term, datetime.date) or isinstance(term, datetime.datetime):
            self.term = calculate_term(start, term)
        else:
            self.term = term

        self.schedule = rrule(freq=MONTHLY, count=self.term, dtstart=self.start_date)
        self.min_payment = (self.loan_amount * self.mpr) / (1 - (1 + self.mpr) ** -self.term)
        self.plan = self.amor_table()
        # print(self.plan)

    def amor_table(self, monthly_payment: float = None, amended_term: int = None):
        """ Generates an amortization chart for the loan, can take multiple values of monthly payments.

        TODO: Associate Datetime with first bill and generate an actual schedule

        Args:
            monthly_payment (float, optional): the monthly payment towards the loan. Defaults to minimum payment.

        Returns:
            pd.Dataframe: dataframe of each monthly payment over the term of the loan
        """
        assert monthly_payment is None or amended_term is None

        # Handle non-default monthly payment
        if monthly_payment is None:
            monthly_payment = self.min_payment
            print(f"{self.name} is using minimum payment of ${monthly_payment}")
        else:
            print(f"{self.name} is using manual payment of ${monthly_payment}")

        # Handle non-default term length
        if amended_term is None:
            term_left = self.term
        else:
            term_left = amended_term
            monthly_payment = (self.loan_amount * self.mpr) / (1 - (1 + self.mpr) ** - amended_term)
            print(f"{self.name} is using amended term of {term_left} months with a minimum payment of ${monthly_payment}")

        headers = ["Date", "Balance Remaining", "Applied to Principal", "Applied to Interest", "Total Interest"]
        payments = [[self.schedule[0], self.principal, 0, 0, 0]]
        total_interest = 0
        balance = self.principal

        # Loop through the payment term
        while balance > monthly_payment and term_left > 0:
            balance, app_principal, app_interest = self.make_payment(balance, monthly_payment)
            total_interest += app_interest

            payments.append([self.schedule[self.term-term_left+1], balance, app_principal, app_interest, total_interest])
            term_left -= 1

        # Convert list of payments to dataframe
        amortization_table = pd.DataFrame(data=payments, columns=headers)
        amortization_table["Date"] = pd.to_datetime(amortization_table["Date"])

        return amortization_table

    def get_balance(self, date: datetime.date) -> float:
        """ Grabs the remaining balance at a given time according to the plan

        FIXME: This should be more generalized, look for matching month and year, not exact datetime
        TODO: Add a class variable for history of payments
        TODO: Separate payments into timeframes. Ex) You expect a pay raise in the future and can increase your payment amount
        TODO: Add error handling for when the requested date doesn't exist

        Args:
            date (datetime.datetime): date of the requested payment

        Returns:
            float: The remaining balance at this stage in the payment plan
        """
        date1 = datetime.datetime(date.year, date.month, 1)
        date2 = datetime.datetime(date.year, date.month + 1, 1)

        # Find the row of the Amortization table for the requested date
        result = self.plan.loc[(self.plan["Date"] >= date1)
                               & (self.plan["Date"] < date2)].reset_index()

        # Extract the balance amount from the table row
        amount = result["Balance Remaining"].get(0)

        # FIXME: Temporary error handling for calling a loan that hasn't been initialized yet
        if amount is None:
            # print(f"Loan ({self.name}) has not started yet!")
            amount = 0

        return amount

    def make_payment(self, principal: float, monthly_payment: float):
        """ Helper function for amor_table()

        Calculates the new principal after making a monthly payment, then

        Args:
            principal (float): original principal
            monthly_payment (float): monthly bill going towards loan (towards both principal and interest)

        Returns:
            tuple: a tuple containing the new principal, the amount applied to principal, and the amount to interest
        """
        # Calculate the amount of interest generated this month
        current_interest_payment = principal * self.mpr
        # Calculate the amount of montly payment that goes towards the principal
        current_principal_payment = monthly_payment - current_interest_payment

        principal -= current_principal_payment

        return [round(principal, 2), round(current_principal_payment, 2), round(current_interest_payment, 2)]


if __name__ == "__main__":
    print("Student Loans:")
    mohela1 = Loan(amount=4500, apr=.035, term=120)
    mohela2 = Loan(amount=5500, apr=.025, term=120)

    # print("Mortgage:")
    mort = Loan(amount=250000, apr=.05, term=120)
    print(mort.amor_table(monthly_payment=3000))
