"""_summary_
"""


class Budget():
    def __init__(self, gross: float):
        # Collect Income and Region
        self.gross_income = gross
        self.taxes = self.calculate_taxes()

        # Adjust income for taxes
        self.income = self.gross_income - self.taxes

    def calculate_taxes(self):
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

        Returns:
            _type_: _description_
            
        """
        return 0

    def __str__(self):
        bgt_str = f"Budget: gross=${self.gross_income}\n"
        bgt_str += f"\t taxes = -$({self.taxes})"
        return bgt_str

if __name__ == "__main__":
    bgt = Budget(104000)
    print(bgt)
