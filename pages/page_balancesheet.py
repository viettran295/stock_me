import dash 
from dash import html, dcc
from utils import dash_utils

layout = html.Div([
            html.H1("Balancesheet", style={"color": dash_utils.colors["text"]})
            ])

