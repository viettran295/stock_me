import stock_me.cashflow as cf
from dash import html, dcc, Input, Output, callback
import yfinance as yf
from utils import dash_utils
import pandas as pd

cf = cf.CashFlow()

layout = html.Div([
            html.H1("Cashflow", style={"color": dash_utils.colors["text"]}),
            dcc.Graph(id="cashflow"),
            ])

@callback(
        Output("cashflow", "figure"),
        Input("search_stock", "value")
)
def show_graph(search_stock):
    dataPath = f"{dash_utils.DATA_PATH}/{search_stock}_cashflow.pkl"
    cashflow = pd.read_pickle(dataPath)
    return cf.show_cashflow(cashflow)