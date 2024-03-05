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
        return 0

    def __str__(self):
        bgt_str = f"Budget: gross=${self.gross_income}\n"
        bgt_str += f"\t taxes = -$({self.taxes})"
        return bgt_str

if __name__ == "__main__":
    bgt = Budget(104000)
    print(bgt)
