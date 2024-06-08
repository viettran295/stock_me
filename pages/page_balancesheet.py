from dash import html, dcc, Input, Output, callback
from utils import dash_utils
import yfinance as yf
import stock_me.balance_sheet as bs 

bs = bs.BalanceSheet()

layout = html.Div([
            html.H1("Balance sheet", style={"color": dash_utils.colors["text"]}),
            dcc.Graph(id="quick_ratio"),
            dcc.Graph(id="equity_to_liability"),
            dcc.Graph(id="asset_structure")
            ])

@callback(
        Output("quick_ratio", "figure"),
        Output("equity_to_liability", "figure"),
        Output("asset_structure", "figure"),
        Input("search_stock", "value")
)
def show_graph(search_stock):
    ticker = yf.Ticker(search_stock)
    balancesheet = ticker.balancesheet
    return [
            bs.show_quick_ratio(balancesheet),
            bs.show_equity_to_liability(balancesheet),
            bs.show_asset_structure(balancesheet)
            ] 