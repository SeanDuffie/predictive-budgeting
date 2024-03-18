class Income():
    def __init__(self, annual: float, state: str):
        self.gross_annual = annual
        self.gross_monthly = annual / 12

        self.calculate_tax()

    def calculate_tax(self):
        pass

if __name__ == "__main__":
    Income(100000, "GA")
