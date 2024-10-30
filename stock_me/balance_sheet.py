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
        
        self.ratio_analysis = ["Current Assets", "Inventory", "Current Liabilities"]
        self.balance_sheet = self.asset_structure + ["Invested Capital"]
        
    def show_asset_structure(self, df: pl.DataFrame):
        df = self.pick_criteria(df, self.asset_structure)
        df = df.melt(id_vars=[self.idx_column], value_vars=[f"{self.currYear - i}" for i in range(self.analyze_years)],
                    variable_name="Year", value_name="Dollars")
        fig = px.bar(df, x="Year", y="Dollars", color=df[self.idx_column], template="plotly_dark",
                    title="Asset Structure", width=800)
        return fig
    
    def show_equity_to_liability(self, df: pl.DataFrame):
        df = self.pick_criteria(df, self.equity_to_liability)
        fig = make_subplots(rows=1, cols=self.analyze_years, 
                            subplot_titles=[f"{self.currYear-i}" for i in range(self.analyze_years)],
                            specs=[[{'type': 'domain'} for _ in range(self.analyze_years)]])
        for i in range(self.analyze_years):
            year = self.currYear - i
            if (df[f"{year}"] > 0).all():
                fig.add_trace(go.Pie(values=df[f"{year}"], labels=df["Criteria"], hole=.3), row=1, col=i+1)

        fig.update_traces(textfont_size=12,
                        marker=dict(line=dict(color='#000000', width=1)))
        fig.update_layout(title="Equity to liability", title_font_size=17, template="plotly_dark",)
        return fig
    
    def show_quick_ratio(self, df: pl.DataFrame):
        """
        Liquidity ratio: current ratio, quick ratio, cash ratio. This graph is only for quick ratio
        Quick ratio = quick assets / current liabilities
        with: quick assets = current assets - inventory
        """
        df = self.pick_criteria(df, self.ratio_analysis)
        if df[self.idx_column].is_in(["Inventory"]).any():
            df = df.melt(id_vars=[self.idx_column], value_vars=[f"{self.currYear- i}" for i in range(self.analyze_years)],
                        variable_name="Year", value_name="Dollars")
            new_df = []
            df = df.drop_nulls()
            for i in range(self.analyze_years-1):
                year = dt.now().year - i
                curr_assets = df.filter((pl.col(self.idx_column) == "Current Assets") & (pl.col("Year") == f"{year}"))
                inventory = df.filter((pl.col(self.idx_column) == "Inventory") & (pl.col("Year") == f"{year}"))
                try:
                    # quick assets = current assets - inventory
                    quick_assets = curr_assets["Dollars"][0] - inventory["Dollars"][0]
                except:
                    self.error_log.error("Inventory does not exist", exc_info=True)
                    continue
                new_row = {
                        self.idx_column: "Quick Assets",
                        "Year": f"{year}",
                        "Dollars": quick_assets
                }
                new_df.append(new_row)
            new_df = pl.DataFrame(new_df)
            df = df.vstack(new_df)
            df = df.sort("Year")
            df = df.filter(pl.col(self.idx_column).is_in(["Current Liabilities", "Quick Assets"]))
            fig = px.bar(df, x="Year", y="Dollars", color=df["Criteria"], template="plotly_dark",
                title="Quick ratio", width=800)
            return fig