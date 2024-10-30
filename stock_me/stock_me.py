import pandas as pd
from datetime import datetime as dt
import polars as pl 
import logging
from typing import List

class StockMe:
    _instace = None 
    logging.basicConfig(level=logging.ERROR)

    def __new__(cls):
        if cls._instace is None:
            cls._instace = super().__new__(cls)
        return cls._instace

    def __init__(self) -> None:
        self.idx_column = "Criteria"
        self.currYear = dt.now().year - 1
        self.analyze_years = 0
        self.error_log = logging

    def pick_criteria(self, df: pd.DataFrame, criteria) -> pl.DataFrame:
        df = pl.from_pandas(self.rename_reset_idx(df, self.idx_column))
        df = df.with_columns(
                    df[self.idx_column].map_elements(lambda x: "Net Profit" 
                                                     if x == "Net Income From Continuing Operation Net Minority Interest" else x,
                                                     return_dtype=pl.Utf8)
                )
        return df.filter(pl.col(f'{self.idx_column}').is_in(criteria))

    def rename_reset_idx(self, df: pd.DataFrame, name: str) -> pd.DataFrame:
        cols_year = []
        self.analyze_years = len(df.columns)
        for i in range(self.analyze_years):
             cols_year.append(f"{self.currYear - i}")
        df = df.set_axis(cols_year, axis="columns")
        df.reset_index(inplace=True)
        return df.rename(columns={'index': name})
    
    def get_value_ofType(self, df: pl.DataFrame, criteria: List[str], get_type: str) -> pl.DataFrame:
        try:
            df = self.pick_criteria(df, criteria)
            return df.filter(pl.col(self.idx_column) == get_type)
        except:
            return None
