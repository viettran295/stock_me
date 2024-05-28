import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output, ctx, callback, State
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
        cashflow = ticker.cashflow
        df = fs.pick_criteria(cashflow, fs.cashflow_criteria)
        return dash_table.DataTable(
                    data=df.to_dicts(),
                    columns=[{'id': c, 'name': c} for c in df.columns],
                    style_header={
                        'backgroundColor': 'rgb(0, 0, 0)',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'border': '1px solid white',
                        },
                    style_data={
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                        },
                    )

if __name__ == '__main__':
    app.run_server(debug=True)