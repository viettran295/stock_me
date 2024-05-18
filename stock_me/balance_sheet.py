import pandas as pd 
from .stock_me import StockMe

class BalanceSheet(StockMe):
    def __init__(self) -> None:
        super().__init__()
        self.asset = ["Current Assets", "Cash And Cash Equivalents", "Receivables", 
                      "Total Non Current Assets", "Net PPE", "Goodwill And Other Intangible Assets", 
                      "Investments And Advances"]

        self.asset_structure = ["Total Liabilities Net Minority Interest", 
                                "Total Equity Gross Minority Interest"]