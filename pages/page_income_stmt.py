import dash 
from dash import html, dcc, Input, callback
from utils import dash_utils

layout = html.Div([
            html.H1("Income statement", style={"color": dash_utils.colors["text"]})
            ])
