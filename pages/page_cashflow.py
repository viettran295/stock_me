import dash 
from dash import html, dcc
from utils import dash_utils

layout = html.Div([
            html.H1("Cashflow", style={"color": dash_utils.colors["text"]})
            ])
