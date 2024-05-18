import pandas as pd 
from .stock_me import StockMe

class BalanceSheet(StockMe):
    def __init__(self) -> None:
        super().__init__()
        self.asset = ["Current Assets", "Cash And Cash Equivalents", "Receivables", 
                      "Total Non Current Assets", "Net PPE", "Goodwill And Other Intangible Assets", 
                      "Investments And Advances"]
    
    def asset_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.rename_reset_Idx(df, self.idx_column)
        return df.loc[df[self.idx_column].isin(self.asset)]