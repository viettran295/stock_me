from dash import (
                Dash, dcc, html, Input, 
                Output, ctx, callback, 
            )
import dash_bootstrap_components as dbc
from pages import page_balancesheet, page_cashflow, page_income_stmt
from utils import dash_utils
import yfinance as yf 
import stock_me.financial_statement as fs
import polars as pl
pl.Config.set_tbl_rows(100)

# Create Dash application
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
app.title = "_Stock Me_"
fs = fs.FinancialStatement()

# Define layout with input to search stock ticker
app.layout = html.Div(
    style={"backgroundColor": dash_utils.colors["background"]},
    children= [
        html.H1("Stock Me app", 
                style={"textAlign": "center",
                        "color": dash_utils.colors["text"]}),
        html.Div("Web app to quickly analyse finacial statement", 
                style={"textAlign": "center",
                        "color": dash_utils.colors["text"]}),
        html.Br(),
        html.Div(
            children=[
                dcc.Input(
                    id="search_stock",
                    type="text",
                    placeholder="ENTER YOUR STOCK",
                    ),
                dbc.Button(
                    id="search_button",
                    children="Search",
                    color="light",
                    href="/"
                    ),
                ],
            style={"display": "flex",
                    "justifyContent": "center"},
            ),
        html.Br(),
        dcc.Location(id="url", pathname="/", refresh=True),
        html.Div(children=[
                    dbc.Button(
                            id="income_stmt_button",
                            children="Income statement",
                            color="outline-light",
                            href="/income_stmt"
                        ),
                    dbc.Button(
                            id="balancesheet_button",
                            children="Balance sheet",
                            color="outline-light",
                            href="/balancesheet"
                        ),
                    dbc.Button(
                            id="cashflow_button",
                            children="Cashflow",
                            color="outline-light",
                            href="/cashflow"
                        ),
                ], className="d-grid gap-4 d-md-flex justify-content-md-center",),
        html.Br(),
        html.Div(id="page_content"),
        # Define layout with DataTable
        html.Div(id="financial_stmt"),
        html.Br(),
            ]
)

@callback(
        Output("page_content", "children"),
        Input("url", "pathname")
)
def route(pathname):
    match pathname:
        case "/income_stmt":
            return page_income_stmt.layout
        case "/balancesheet":
            return page_balancesheet.layout
        case "/cashflow":
            return page_cashflow.layout
        case "/":
            app.layout

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