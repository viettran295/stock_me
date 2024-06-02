import polars as pl
import plotly.express as px
from datetime import datetime as dt
from .stock_me import StockMe

class CashFlow(StockMe):
    def __init__(self) -> None:
        super().__init__()
        self.cash_flow = ["Operating Cash Flow", "Investing Cash Flow", 
                          "Financing Cash Flow", "End Cash Position"]
        
    def show_cashflow(self, df: pl.DataFrame):
        df = self.pick_criteria(df, self.cash_flow)
        df = df.melt(id_vars=[self.idx_column], value_vars=[f"{dt.now().year - i}" for i in range(self.analyze_years)],
                    variable_name="Year", value_name="Dollars")
        fig = px.bar(x=df["Year"], y=df["Dollars"], color=df[self.idx_column], template="plotly_dark",
                    title="Cash flow", width=800)
        return fig