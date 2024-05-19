import pandas as pd 
from .stock_me import StockMe
from datetime import datetime as dt
import plotly.express as px

class BalanceSheet(StockMe):
    def __init__(self) -> None:
        super().__init__()
                        # Current assets
        self.asset = ["Cash And Cash Equivalents", "Receivables", "Prepaid Assets", "Other Current Assets", "Restricted Cash", 
                        # Non-current assets
                      "Net PPE", "Goodwill And Other Intangible Assets", "Investments And Advances", "Non Current Deferred Assets", "Non Current Prepaid Assets", "Other Non Current Assets"]

        self.asset_structure = ["Total Liabilities Net Minority Interest", 
                                "Total Equity Gross Minority Interest"]
        
    def show_asset_structure(self, df: pd.DataFrame):
        years = 4
        df = self.pick_criteria(df, self.asset)
        df = pd.melt(df, id_vars=[self.idx_column], value_vars=[f"{dt.now().year - i}" for i in range(years)],
                    var_name="Year", value_name="Dollars")
        fig = px.bar(df, x=df["Year"], y=df["Dollars"], color=df[self.idx_column],
                    title="Asset Structure", width=800)
        fig.show()