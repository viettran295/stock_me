import polars as pl
import plotly.graph_objects as go
from .stock_me import StockMe

class FinancialStatement(StockMe):
    def __init__(self) -> None:
        super().__init__()
        self.income_criteria = ['Gross Profit', 'Cost Of Revenue', 'Total Revenue', 'Total Expenses', 
                       'Interest Expense', 'Operating Revenue', 'Pretax Income', 'EBITDA', 'EBIT', 
                       'Tax Provision', 'Diluted EPS', 'Basic EPS',
                       'Net Income From Continuing Operation Net Minority Interest']
        self.balancesheet_criteria = ['Total Assets', 'Total Liabilities Net Minority Interest',  
                         'Total Equity Gross Minority Interest', 'Total Capitalization', 
                         'Total Debt', 'Current Debt', 'Investments And Advances', 'Cash And Cash Equivalents']
        self.cashflow_criteria = ['Operating Cash Flow', 'Investing Cash Flow', 
                                  'Financing Cash Flow', 'Free Cash Flow']
    
    @staticmethod
    def calculate_growing(df: pl.DataFrame) -> pl.DataFrame:
        nums_cols = len(df.columns) - 1
        for i in range(1, nums_cols):
            grow_df = (df[df.columns[i]] - df[df.columns[i+1]]) / df[df.columns[i+1]] * 100
            df = df.with_columns(
                (pl.lit(grow_df)).alias(f"Growing {df.columns[i]}")
            )
        return df
    
    def show_growing(self, df: pl.DataFrame):
        df = self.calculate_growing(df)
        growing_col_idx = 5
        nums_rows = df[self.idx_column].count()
        fig = go.Figure()
        for i in range(nums_rows):
                fig.add_trace(go.Scatter(
                                x=df.columns[growing_col_idx:], y=df.row(i)[growing_col_idx:],
                            name=df[i, 0]))
        fig.update_layout(title="% Growing", title_font_size=30, 
                        title_x=0.4, title_y=0.99, template="plotly_dark",)
        fig.show()