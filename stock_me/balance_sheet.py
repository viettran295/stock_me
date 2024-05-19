import polars as pl
from .stock_me import StockMe
from datetime import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class BalanceSheet(StockMe):
    def __init__(self) -> None:
        super().__init__()
                        # Current assets
        self.asset_structure = ["Cash And Cash Equivalents", "Receivables", "Prepaid Assets", "Other Current Assets", "Restricted Cash", 
                        # Non-current assets
                      "Net PPE", "Goodwill And Other Intangible Assets", "Investments And Advances", "Non Current Deferred Assets", "Non Current Prepaid Assets", "Other Non Current Assets"]

        self.equity_to_liability = ["Total Liabilities Net Minority Interest", 
                                "Total Equity Gross Minority Interest"]
        
    def show_asset_structure(self, df: pl.DataFrame):
        df = self.pick_criteria(df, self.asset_structure)
        df = df.melt(id_vars=[self.idx_column], value_vars=[f"{dt.now().year - i}" for i in range(self.analyze_years)],
                    variable_name="Year", value_name="Dollars")
        fig = px.bar(x=df["Year"], y=df["Dollars"], color=df[self.idx_column], template="plotly_dark",
                    title="Asset Structure", width=800)
        fig.show()
    
    def show_equity_to_liability(self, df: pl.DataFrame):
        df = self.pick_criteria(df, self.equity_to_liability)
        fig = make_subplots(rows=1, cols=self.analyze_years, 
                            subplot_titles=[f"{self.currYear-i}" for i in range(self.analyze_years)],
                            specs=[[{'type': 'domain'} for _ in range(self.analyze_years)]])
        for i in range(self.analyze_years):
            year = self.currYear - i
            fig.add_trace(go.Pie(values=df[f"{year}"], labels=df["Criteria"], hole=.3), row=1, col=i+1)

        fig.update_traces(textfont_size=12,
                        marker=dict(line=dict(color='#000000', width=1)))
        fig.update_layout(title="Equity to liability", title_font_size=30, 
                        title_x=0.4, title_y=0.99, template="plotly_dark",)
        fig.show()