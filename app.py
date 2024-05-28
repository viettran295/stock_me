from dash import (
                Dash, dcc, html, Input, 
                Output, ctx, callback, 
            )
from utils import dash_utils
import yfinance as yf 
import stock_me.financial_statement as fs
import polars as pl
pl.Config.set_tbl_rows(100)

# Create Dash application
app = Dash(__name__)
app.title = "_Stock Me_"
fs = fs.FinancialStatement()

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Define layout with input to search stock ticker
app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children= [
        html.H1("Stock Me app", 
                style={"textAlign": "center",
                        "color": colors["text"]}),
        html.Div("Web app to quickly analyse finacial statement", 
                style={"textAlign": "center",
                        "color": colors["text"]}),
        html.Br(),
        html.Div(
            children=[
                dcc.Input(
                    id="search_stock",
                    type="text",
                    placeholder="ENTER YOUR STOCK",
                    ),
                html.Button("Search", id="search_button"),
                ],
            style={"display": "flex",
                    "justifyContent": "center"},
            ),
        html.Br(),
        # Define layout with DataTable
        html.Div(id="financial_stmt")
            ]
)


@callback(
    Output("financial_stmt", "children"),
    Input("search_button", "n_clicks"),
    Input("search_stock", "value")
)
def search_stock(_, search_stock):
    if "search_button" == ctx.triggered_id:
        ticker = yf.Ticker(f"{search_stock}")
        financial_stmts = {
            'income': ticker.incomestmt,
            'balancesheet': ticker.balancesheet,
            'cashflow': ticker.cashflow
        }
        
        criteria = {
            'income': fs.income_criteria,
            'balancesheet': fs.balancesheet_criteria,
            'cashflow': fs.cashflow_criteria
        }
        
        tables = []
        for stmt, data in financial_stmts.items():
            df = fs.pick_criteria(data, criteria[stmt])
            table = dash_utils.factory_DashTable(df)
            tables.append(table)
        return html.Div(tables)

if __name__ == '__main__':
    app.run_server(debug=True)