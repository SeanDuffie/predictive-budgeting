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

        self.taxes = self.calculate_tax(state=state)

        self.net_annual = self.gross_annual - self.taxes
        self.net_monthly = self.net_annual / 12
        self.net_weekly = self.net_annual / 52

    def calculate_tax(self, state: str):
        """_summary_

        Resources:
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
