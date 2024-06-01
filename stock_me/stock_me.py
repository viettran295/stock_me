import pandas as pd
from datetime import datetime as dt
import polars as pl 

class StockMe:
    _instace = None 

    def __new__(cls):
        if cls._instace is None:
            cls._instace = super().__new__(cls)
        return cls._instace

    def __init__(self) -> None:
        self.idx_column = "Criteria"
        self.currYear = dt.now().year
        self.analyze_years = 0

    def pick_criteria(self, df: pd.DataFrame, criteria) -> pl.DataFrame:
        df = pl.from_pandas(self.rename_reset_idx(df, self.idx_column))
        return df.filter(pl.col(f'{self.idx_column}').is_in(criteria))

    def rename_reset_idx(self, df: pd.DataFrame, name: str) -> pd.DataFrame:
        cols_year = []
        self.analyze_years = len(df.columns)
        for i in range(self.analyze_years):
             cols_year.append(f"{self.currYear - i}")
        df = df.set_axis(cols_year, axis="columns")
        df.reset_index(inplace=True)
        return df.rename(columns={'index': name})