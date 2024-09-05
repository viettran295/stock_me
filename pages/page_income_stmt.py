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
            ])

@callback(
        Output("growing_graph", "figure"),
        Output("profitability_graph", "figure"),
        Input("search_stock", "value")
)
def show_graph(search_stock):
        dataPath = f"{dash_utils.DATA_PATH}/{search_stock}_incomestmt.csv"
        income = pd.read_csv(dataPath, index_col=0)
        return  [
                fs.show_growing(income),
                fs.show_profitability_ratios(income),
                ]
