import pandas as pd
from datetime import datetime as dt

class StockMe:
    def __init__(self) -> None:
        self.idx_column = "Criteria"
        self.currYear = dt.now().year
        self.analyze_years = 4

    def pick_criteria(self, df: pd.DataFrame, criteria) -> pd.DataFrame:
        df = self.rename_reset_idx(df, self.idx_column)
        return df.loc[df[self.idx_column].isin(criteria)]
    
    def rename_reset_idx(self, df: pd.DataFrame, name: str) -> pd.DataFrame:
        years = 4
        cols_year = []
        for i in range(years):
             cols_year.append(f"{self.currYear - i}")
        df = df.set_axis(cols_year, axis="columns")
        df.reset_index(inplace=True)
        return df.rename(columns={'index': name})