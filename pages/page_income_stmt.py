from dash import html, dcc, Input, Output, callback
from utils import dash_utils
import stock_me.income_stmt as fs
import yfinance as yf 

fs = fs.FinancialStatement()

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
        ticker = yf.Ticker(search_stock)
        income = ticker.incomestmt
        return  [
                fs.show_growing(income),
                fs.show_profitability_ratios(income),
                ]
