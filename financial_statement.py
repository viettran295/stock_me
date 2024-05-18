import pandas as pd 
import plotly.graph_objects as go
from datetime import datetime

class FinancialStatement:
    def __init__(self) -> None:
        self.idx_column = "Criteria"
        self.income_criteria = ['Gross Profit', 'Cost Of Revenue', 'Total Revenue', 'Total Expenses', 
                       'Interest Expense', 'Operating Revenue', 'Pretax Income', 'EBITDA', 'EBIT', 
                       'Tax Provision', 'Diluted EPS', 'Basic EPS',
                       'Net Income From Continuing Operation Net Minority Interest']
        self.balancesheet_criteria = ['Total Assets', 'Total Liabilities Net Minority Interest',  
                         'Total Equity Gross Minority Interest', 'Total Capitalization', 
                         'Total Debt', 'Current Debt', 'Investments And Advances', 'Cash And Cash Equivalents']
        self.cashflow_criteria = ['Operating Cash Flow', 'Investing Cash Flow', 
                                  'Financing Cash Flow', 'Free Cash Flow']
    
    def incomestmt_df(self, df: pd.DataFrame) -> pd.DataFrame:
         df = self.rename_reset_Idx(df, self.idx_column)
         return df.loc[df[self.idx_column].isin(self.income_criteria)]
    
    def balancesheet_df(self, df: pd.DataFrame) -> pd.DataFrame:
         df = self.rename_reset_Idx(df, self.idx_column)
         return df.loc[df[self.idx_column].isin(self.balancesheet_criteria)]

    def cashflow_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.rename_reset_Idx(df, self.idx_column)
        return df.loc[df[self.idx_column].isin(self.cashflow_criteria)]

    @staticmethod
    def rename_reset_Idx(df: pd.DataFrame, name: str) -> pd.DataFrame:
        current_year = datetime.now().year
        years = 4
        cols_year = []
        for i in range(years):
             cols_year.append(f"{current_year - i}")
        df = df.set_axis(cols_year, axis="columns")
        df.reset_index(inplace=True)
        return df.rename(columns={'index': name})
    
    @staticmethod
    def calculate_growing(df: pd.DataFrame) -> pd.DataFrame:
        nums_cols = len(df.columns) - 1
        for i in range(1, nums_cols):
            grow_df = (df[df.columns[i]] - df[df.columns[i+1]]) / df[df.columns[i+1]] * 100
            df["% Growing " + str(df.columns[i]).split()[0]] = grow_df
        return df
    
    @staticmethod
    def show_growing(df: pd.DataFrame):
        fig = go.Figure()
        growing_col = 4
        for i in range(len(df.index)):
                fig.add_trace(go.Scatter(
                                x=df.columns[:growing_col:-1], y=df.iloc[i][:growing_col:-1],
                                name=df.iloc[i][0]))
        fig.show()