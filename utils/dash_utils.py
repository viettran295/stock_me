from dash.dash_table import DataTable, FormatTemplate
import polars as pl 

def factory_DashTable(df: pl.DataFrame):
    return DataTable(
                data=df.to_dicts(),
                columns=[{'id': c, 'name': c, 'type': 'numeric', 'format': FormatTemplate.money(2)} for c in df.columns],
                style_cell={
                    'textAlign': 'left',
                    'width': '180px',
                    },
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