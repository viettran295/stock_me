import pandas as pd 

class FinancialStatement:
    def __init__(self) -> None:
        self.financial_criteria = ['Gross Profit', 'Cost Of Revenue', 'Total Revenue', 'Total Expenses', 
                       'Interest Expense', 'Operating Revenue', 'Pretax Income', 'EBITDA', 'EBIT', 
                       'Tax Provision', 'Diluted EPS', 'Basic EPS',
                       'Net Income From Continuing Operation Net Minority Interest']
        self.balancesheet_criteria = ['Total Assets', 'Total Liabilities Net Minority Interest',  
                         'Total Equity Gross Minority Interest', 'Total Capitalization', 
                         'Net Debt', 'Total Debt', 'Current Debt', 
                         'Investments And Advances', 'Cash And Cash Equivalents']
        self.cashflow_criteria = ['Operating Cash Flow', 'Investing Cash Flow', 
                                  'Financing Cash Flow', 'Free Cash Flow']
    
    @staticmethod
    def calculate_growing(df: pd.DataFrame) -> pd.DataFrame:
        nums_cols = len(df.columns) - 1
        for i in range(nums_cols):
            grow_df = (df[df.columns[i]] - df[df.columns[i+1]]) / df[df.columns[i+1]] * 100
            df["% Growing " + str(df.columns[i]).split()[0]] = grow_df
        return df