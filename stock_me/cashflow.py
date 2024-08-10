import polars as pl
import plotly.express as px
import plotly.graph_objects as go 
from datetime import datetime as dt
from .stock_me import StockMe

class CashFlow(StockMe):
    def __init__(self) -> None:
        super().__init__()
        self.cash_flow = ["Operating Cash Flow", "Investing Cash Flow", 
                          "Financing Cash Flow", "End Cash Position"]
        
    def show_cashflow(self, df: pl.DataFrame):
        """
        Visulize cash flow types
        """
        df = self.pick_criteria(df, self.cash_flow)
        df = df.melt(id_vars=[self.idx_column], value_vars=[f"{dt.now().year - i}" for i in range(self.analyze_years)],
                    variable_name="Year", value_name="Dollars")
        fig = px.bar(df, x="Year", y="Dollars", color=df[self.idx_column], template="plotly_dark",
                    title="Cash flow", width=800)
        # Aggregate net cash flow by year
        df_agg = df.group_by("Year").agg(pl.col("Dollars").sum()).sort(by="Year")
        fig.add_trace(go.Scatter(x=df_agg["Year"], y=df_agg["Dollars"], name="Net cash flow"))
        fig.update_layout(legend_title_text="Cash flow types")
        return fig