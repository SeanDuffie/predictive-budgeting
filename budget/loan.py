""" @file loan.py
    @author Sean Duffie
    @brief This Loan object is intended to help me organize loan-related features of my budget

    References:
    - https://www.bankrate.com/mortgages/amortization-calculator/
"""
import pandas as pd


class Loan():
    """ The Loan object allows me to store data related to loans without having to retype
        it every time I want to try to experiment with new parameters
    """
    def __init__(self, amount: float, apr: float, term: int, name: str = "Loan"):
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

        self.term = term
        self.min_payment = (self.loan_amount * self.mpr) / (1 - (1 + self.mpr) ** -self.term)

    def amor_table(self, monthly_payment: float = None):
        """ Generates an amortization chart for the loan, can take multiple values of monthly payments.

        TODO: Associate Datetime with first bill and generate an actual schedule

        Args:
            monthly_payment (float, optional): the monthly payment towards the loan. Defaults to minimum payment.

        Returns:
            pd.Dataframe: dataframe of each monthly payment over the term of the loan
        """
        if monthly_payment is None:
            print(f"Using minimum payment of ${self.min_payment}")
            monthly_payment = self.min_payment

        payments = [[self.principal, 0, 0, 0]]
        total_interest = 0
        prin = self.principal
        term_left = self.term

        # Loop through the payment term
        while prin > monthly_payment and term_left > 0:
            payment = self.make_payment(prin, monthly_payment)

            prin = payment[0]
            term_left -= 1
            total_interest += payment[2]

            payment.append(total_interest)
            payments.append(payment)

        # Convert list of payments to dataframe
        amortization_table = pd.DataFrame(data=payments,
                                        columns=['Principal Remaining',
                                                'Current Principal Payment',
                                                'Current Interest Payment',
                                                'Total Interest Paid'])

        return amortization_table

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
    # mohela1 = Loan(4500, .035, 120)
    # mohela2 = Loan(5500, .025, 120)
    # print(mohela1.amor_table(750))
    # print(mohela2.amor_table(750))
    # mohela.amor_table(1000)

    print("Mortgage:")
    mort = Loan(250000, .06, 180)
    print(mort.amor_table())
    print(mort.amor_table(2500))
    print(mort.amor_table(3500))
