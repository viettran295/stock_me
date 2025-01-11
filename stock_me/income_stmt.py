import polars as pl
import plotly.graph_objects as go
import plotly.express as px
from .stock_me import StockMe
from plotly.subplots import make_subplots
from .balance_sheet import BalanceSheet

class IncomeStatement(StockMe):
    def __init__(self) -> None:
        super().__init__()
        self.income_criteria = ['Gross Profit', 'Total Revenue', 'EBITDA', 'EBIT', 'Net Income']
        self.profitability_ratios = ["Total Revenue", "Operating Income", "Gross Profit", "Net Income"]
    
    @staticmethod
    def calculate_growing(df: pl.DataFrame) -> pl.DataFrame:
        """
        Calculate percent growing of income criteria
        """
        nums_cols = len(df.columns) - 1
        for i in range(1, nums_cols):
            grow_df = (df[df.columns[i]] - df[df.columns[i+1]]) / df[df.columns[i+1]] * 100
            df = df.with_columns(
                (pl.lit(grow_df)).alias(f"Growing {df.columns[i]}")
            )
        return df
    
    def show_growing(self, df: pl.DataFrame):
        """
        Visualize percent growing of metrics
        """
        df = self.pick_criteria(df, self.income_criteria)
        df = self.calculate_growing(df)
        growing_col_idx = 5
        nums_rows = df[self.idx_column].count()
        fig = go.Figure()
        for i in range(nums_rows):
                fig.add_trace(go.Scatter(
                                x=df.columns[growing_col_idx:], y=df.row(i)[growing_col_idx:],
                            name=df[i, 0]))
        fig.update_layout(title="% Growing", title_font_size=30, 
                        title_x=0.47, title_y=0.99, template="plotly_dark",)
        return fig
    
    def show_profitability_ratios(self, df: pl.DataFrame):
        """
        Visualize profitability ratios: 
            - Gross profit margin = revenue - COGS (cost of goods sold)
            - Operating profit margin = gross profit - operating expenses - depreciation (tangible assets) - amortization (intagible items)
            - Net profit margin = operating profit - tax - interest
        """
        df = self.pick_criteria(df, self.profitability_ratios)
        years = df.columns[1:]
        col = 1
        fig = make_subplots(rows=1, cols=len(years), shared_yaxes=True)
        # Extract total revenue in 3 years from data frame
        revenue = df.filter(pl.col(self.idx_column) == "Total Revenue").select(pl.exclude(self.idx_column))
        for year in years:
            # Calculate margin (ratio of profit to revenue)
            fig.add_trace(go.Bar(x=df[self.idx_column], y=(df[year] / revenue[year][0]) * 100, name=year), 1, col)
            fig.update_xaxes(title_text=year, row=1, col=col)
            col += 1
        fig.update_yaxes(title_text="Dollars", row=1, col=1,)
        fig.update_layout(title="Profitability ratios margin", title_font_size=30, 
                                title_x=0.5, title_y=0.99, template="plotly_dark",)
        return fig

    def show_ROI(self, df_incstmt: pl.DataFrame, df_bs: pl.DataFrame):
        bs = BalanceSheet()
        net_profit = self.get_value_ofType(df_incstmt, self.income_criteria, "Net Income")
        investment = self.get_value_ofType(df_bs, bs.balance_sheet, "Invested Capital") 
        years = net_profit.columns[1:]
        ROI_df = pl.DataFrame({self.idx_column: "ROI"})
        for year in years: 
            try:
                ROI_df = ROI_df.with_columns((net_profit.select(pl.col(year)) / investment.select(pl.col(year).abs())) * 100)
            except:
                self.error_log.error("Fail to calculate ROI", exc_info=True)
        fig = px.bar(ROI_df, x=self.idx_column, y=years, barmode='group')
        fig.update_layout(title="ROI - Return on Investment", template="plotly_dark",
                         title_font_size=30, title_x=0.5, title_y=0.99)
        return fig

    #TODO: implement ROA, ROE, ROI, EBITDA and compare to others
    #TODO: Asset turnover ratio, Inventory turnover ratio
    # ?: Amortization for intangible assets
    # ?: Expense negative / positive
    # ?: ROI for investment cash flow