import pandas as pd 
from .stock_me import StockMe
from datetime import datetime as dt
import plotly.express as px

class BalanceSheet(StockMe):
    def __init__(self) -> None:
        super().__init__()
        self.asset = ["Current Assets", "Cash And Cash Equivalents", "Receivables", 
                      "Total Non Current Assets", "Net PPE", "Goodwill And Other Intangible Assets", 
                      "Investments And Advances"]

        self.asset_structure = ["Total Liabilities Net Minority Interest", 
                                "Total Equity Gross Minority Interest"]
        
    def show_asset_structure(self, df: pd.DataFrame):
        years = 4
        df = pd.melt(df, id_vars=[self.idx_column], value_vars=[f"{dt.now().year - i}" for i in range(years)],
                    var_name="Year", value_name="Dollars")
        fig = px.bar(df, x=df["Year"], y=df["Dollars"], color=df[self.idx_column],
                    title="Asset Structure", width=800)
        fig.show()