"""_summary_
    References:
    - https://www.bankrate.com/mortgages/amortization-calculator/
"""

class Loan():
    def __init__(self, amount: float, apr: float, term: int, name: str = "Loan"):
        self.loan_amount = amount
        self.principal = amount
        self.apr = apr
        self.mpr = apr / 12

        self.interest_table = []
        self.principal_table = []
        self.total_interest = 0

        payments = [[principal, 0, 0, 0]]
        total_interest = 0

        while self.principal > 0 and term_remaining > 0:
            payment = make_payment(monthly_payment)
            principal = payment[0]
            term_remaining -= 1
            total_interest += payment[2]
            payment.append(total_interest)
            payments.append(payment)

        amortization_table = pd.DataFrame(data=payments,
                                        columns=['Principal Remaining',
                                                'Current Principal Payment',
                                                'Current Interest Payment',
                                                'Total Interest Paid'])
        return amortization_table

    def make_payment(self, monthly_payment):
        interest = self.principal*self.apr/12

    def minimum_payment(self, timeframe):
        pass

if __name__ == "__main__":
    Loan(10000, .033, 120)
