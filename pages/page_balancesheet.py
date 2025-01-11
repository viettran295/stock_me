from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from utils import dash_utils
import yfinance as yf
import stock_me.balance_sheet as bs 
import pandas as pd

bs = bs.BalanceSheet()

layout = html.Div([
            html.H1("Balance sheet", style={"color": dash_utils.colors["text"]}),
            dbc.Alert(
                        "Quick ratio graph is not available \
                        because inventory does not exist in balance sheet",
                        id="alert_no_inventory",
                        dismissable=True,
                        fade=True,
                        is_open=False,
                        ),
            dcc.Graph(id="quick_ratio"),
            dcc.Graph(id="equity_to_liability"),
            dcc.Graph(id="asset_structure")
            ])

@callback(
        Output("alert_no_inventory", "is_open"),
        Output("quick_ratio", "figure"),
        Output("equity_to_liability", "figure"),
        Output("asset_structure", "figure"),
        Input("search_stock", "value"),
        State("alert_no_inventory", "is_open")
)
def show_graph(search_stock, is_open):
        dataPath = f"{dash_utils.DATA_PATH}/{search_stock}_balancesheet.pkl"
        balancesheet = pd.read_pickle(dataPath)
        if "Inventory" in balancesheet.index:
                is_open = False
        else:
                is_open = True
        return [
                is_open,
                bs.show_quick_ratio(balancesheet),
                bs.show_equity_to_liability(balancesheet),
                bs.show_asset_structure(balancesheet)
                ]