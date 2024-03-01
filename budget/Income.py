class Income():
    def __init__(self, annual: float):
        self.gross_annual = annual
        self.gross_monthly = annual / 12
        
        self.calculate_tax()
        
    def calculate_tax(self):
        pass
    