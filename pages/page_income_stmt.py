from dash import html, dcc, Input, Output, callback
from utils import dash_utils
import stock_me.income_stmt as fs
import yfinance as yf 
import pandas as pd 
from utils import dash_utils

fs = fs.IncomeStatement()

layout = html.Div([
            html.H1("Income statement", style={"color": dash_utils.colors["text"]}),
            dcc.Graph(id='growing_graph'),
            dcc.Graph(id='profitability_graph'),
            dcc.Graph(id='ROI'),
            ])

@callback(
        Output("growing_graph", "figure"),
        Output("profitability_graph", "figure"),
        Output("ROI", "figure"),
        Input("search_stock", "value")
)
def show_graph(search_stock):
        dataPath = f"{dash_utils.DATA_PATH}/{search_stock}_incomestmt.pkl"
        income = pd.read_pickle(dataPath)
        bs_dataPath = f"{dash_utils.DATA_PATH}/{search_stock}_balancesheet.pkl"
        is_dataPath = f"{dash_utils.DATA_PATH}/{search_stock}_incomestmt.pkl"
        balancesheet = pd.read_pickle(bs_dataPath)
        incomestmt = pd.read_pickle(is_dataPath)
        return  [
                fs.show_growing(income),
                fs.show_profitability_ratios(income),
                fs.show_ROI(incomestmt, balancesheet)
                ]
