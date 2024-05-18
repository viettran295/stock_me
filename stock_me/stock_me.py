import pandas as pd
from datetime import datetime

class StockMe:
    def __init__(self) -> None:
        self.idx_column = "Criteria"

    def pick_criteria(self, df: pd.DataFrame, criteria) -> pd.DataFrame:
        df = self.rename_reset_Idx(df, self.idx_column)
        return df.loc[df[self.idx_column].isin(criteria)]
    
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