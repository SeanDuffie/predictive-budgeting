"""_summary_
    References:
    - https://www.bankrate.com/mortgages/amortization-calculator/
"""
import pandas as pd

class Loan():
    def __init__(self, amount: float, apr: float, term: int, name: str = "Loan"):
        self.name = name
        self.loan_amount = amount
        self.principal = amount
        self.apr = apr
        self.mpr = apr / 12

        self.term = term
        self.min_payment = (self.loan_amount * self.mpr) / (1 - (1 + self.mpr) ** -self.term)
        print(f"{self.min_payment=}")

        self.interest_table = []
        self.principal_table = []
        self.total_interest = 0


    def amor_table(self, monthly_payment = None):
        if monthly_payment is None:
            monthly_payment = self.min_payment

        payments = [[self.principal, 0, 0, 0]]
        total_interest = 0
        prin = self.principal
        term_left = self.term

        while prin > 0 and term_left > 0:
            payment = self.make_payment(prin, monthly_payment)

            prin = payment[0]
            term_left -= 1
            total_interest += payment[2]

            payment.append(total_interest)
            payments.append(payment)

        amortization_table = pd.DataFrame(data=payments,
                                        columns=['Principal Remaining',
                                                'Current Principal Payment',
                                                'Current Interest Payment',
                                                'Total Interest Paid'])
        print(amortization_table)

    def make_payment(self, principal, monthly_payment):
        # Calculate the amount of interest generated this month, then the amount applied to they 
        current_interest_payment = principal * self.mpr
        current_principal_payment = monthly_payment - current_interest_payment

        principal -= current_principal_payment

        return [round(principal, 2), round(current_principal_payment, 2), round(current_interest_payment, 2)]


if __name__ == "__main__":
    print("Student Loans:")
    mohela = Loan(10000, .033, 120)
    mohela.amor_table()
    mohela.amor_table(500)
    mohela.amor_table(1000)

    mort = Loan(300000, .06, 180)
    mort.amor_table()
    mort.amor_table(2500)
    mort.amor_table(3500)
