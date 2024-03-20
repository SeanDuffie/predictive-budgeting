"""_summary_
"""

class Income():
    """_summary_
    
    TODO: Add arguments for self-employed, or other special cases
    """
    def __init__(self, annual: float, state: str, **flags):
        # TODO: Implement flags
        for key, value in flags.items():
            print("{}: {}".format(key,value))

        self.gross_annual = annual
        self.gross_monthly = annual / 12
        self.gross_weekly = self.gross_annual / 52

        self.deductibles = []
        self.agi = self.gross_annual
        self.state = state

        self.taxes = self.calculate_tax()

        self.net_annual = self.gross_annual - self.taxes
        self.net_monthly = self.net_annual / 12
        self.net_weekly = self.net_annual / 52

    def add_deductible(self, deduct: float):
        """ Track deductibles here to properly estimate your AGI for tax responsibility

        TODO: Itemize the deductibles more, rather than just a raw float

        Terms:
            - Gross Income - amount of income before any taxes
            - AGI - Adjusted Gross Income, gross income minus some deductions
            - MAGI - Modified Adjusted Gross Income, TODO

        NOTE: What is Taxable Income?
            1. Retirement contributions
                a. Individual Retirement Account (IRA)
                b. Self-employed retirement contributions
                c. 
            2. Charitable Donations (up to 60% of AGI)
            3. Education Expenses
            4. Student Loan Interest
            5. Mortgage Interest ($750,000 or less)
            6. Medical expenses (over 7.5% AGI)
            7. State and local Income Tax
            8. *Personal* Property Tax or Sales taxes (up to IRS threshold)
            9. Gambling/Investment losses
        NOTE: You should itemize deductions if the expenses are greater than the Standard Deduction

        Resources:
            - https://www.investopedia.com/ask/answers/051115/what-difference-between-magi-modified-adjusted-gross-income-and-adjusted-gross-income.asp
            - https://www.investopedia.com/terms/i/itemizeddeduction.asp
            - https://www.hrblock.com/tax-center/income/how-to-calculate-taxable-income/

        Args:
            deduct (float): Amount being deducted from Gross Income
        """
        self.agi = self.gross_annual
        self.deductibles.append(deduct)

        for expense in self.deductibles:
            self.agi -= expense
        print(f"Adjusted Gross Income (AGI): ${self.agi}")

        self.taxes = self.calculate_tax()

    def calculate_tax(self):
        """ Use this function to calculate tax liability, you should already know AGI prior to call

        Resources:
        - https://www.hrblock.com/tax-center/income/how-to-calculate-taxable-income/
        - https://www.irs.gov/individuals/tax-withholding-estimator
        - https://smartasset.com/taxes/income-taxes
        - Federal: 
        - FICA: https://smartasset.com/taxes/all-about-the-fica-tax
            FICA (Federal Insurance Contributions Act) is a tax that funds Social Security and
            Medicare. This tax about 15.3% of the worker's gross income, and is split between the
            Employer and Employee. (About 7.65% for just the Employee). Self-Employed workers are
            stuck with the full 15.3%, however they can deduct the extra half when filing taxes.
            12.4% goes towards Social Security, 2.9% goes towards Medicare.

            There is a cap on the amount of income taxed for Social Security (~$168,600 for 2024),
            however there is no cap on Medicare, and there is an additional Medicare Tax that
            high-income individuals must pay (+0.9%).
        - State: 
        - Local: 

        Args:
            state (str): state of residence for paying taxes

        Returns:
            float: amount of taxes to deduct from gross
            
        """
        state_tax = self.gross_annual * 0.0525
        federal_tax = self.gross_annual * 0.24

        tax_burden = state_tax + federal_tax

        return tax_burden

    def __str__(self) -> str:
        bgt_str = f"Gross = ${self.gross_annual}\n"
        bgt_str += f"\t-taxes = -$({self.taxes})\n"
        bgt_str += f"Net = $({self.net_annual})\n"
        bgt_str += f"\t Per Month = $({self.net_monthly})\n"
        bgt_str += f"\t Per Week = $({self.net_weekly})\n"

        return bgt_str

if __name__ == "__main__":
    print(Income(104000, "GA"))
