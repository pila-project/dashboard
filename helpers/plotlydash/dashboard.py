"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from .data import CreateDataFrame #changed from create_dataframe
from .layout import html_layout
import plotly.express as px
import datetime

from google.cloud import firestore



def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
            'https://fonts.googleapis.com/css?family=Lato'
        ]
    )

    # Custom HTML layout
    dash_app.index_string = html_layout

    # dash_app.layout = ServeLayout

    dash_app.layout = html.Div(
        children=[
            dcc.Graph(
            id='bar-graph'),

            html.H1('The time is: ' + str(datetime.datetime.now())),

            dash_table.DataTable(
                id='data-table',
                sort_action="native",
                sort_mode='native',
                page_size=300),

            dcc.Interval(
            id = 'track-interval',
                interval = 5 * 1000,  # in milliseconds,
                n_intervals = 0),
        ],
        id='dash-container'
    )

    init_callbacks(dash_app)

    return dash_app.server

#        html.Div(id='live-update-text'),


def init_callbacks(dash_app):
    @dash_app.callback(
        [Output('bar-graph', 'figure'), Output('data-table','data'), Output('data-table','columns') ],
        [Input('track-interval', 'n_intervals')]
    )
    def update_graphs(rows):
        # Callback logic
        df = CreateDataFrame(collection_name="karelDB")

        fig = px.bar(df, x='Action', y='Count')

        fig.update_layout(transition_duration=500)

        data = df.to_dict('records')

        columns = [{"name": i, "id": i} for i in df.columns]

        return fig, data, columns





# def ServeLayout():
#     return html.Div(
#         children=[dcc.Graph(
#             id='bar-graph',
#             figure=fig),
#             CreateDataTable(df),
#             html.H1('The time is: ' + str(datetime.datetime.now()))
#         ],
#         id='dash-container'
#     )



