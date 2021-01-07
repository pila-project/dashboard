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
import datetime, time
from .filemanager import FirestoreListener, CreateTable, IndexFlattener, DataBars, MaxValueTableStyler, IntermediateDataMaker
from google.cloud import firestore
from collections import Counter
from .tabs import Table

import json
import dash_building_blocks as dbb


def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
            'https://fonts.googleapis.com/css?family=Lato',
            'https://codepen.io/chriddyp/pen/bWLwgP.css'
        ]
    )

    ms_interval = 6 * 1000

    table_metrics = ['attempts','success']
    tab_names = ['tab1', 'tab2']
    tables = [Table(app=dash_app, data={'name': name, 'tab':tab_names[0]}) for name in table_metrics]

    store = dbb.Store(dash_app)
    store.register('intermediate-data')

    # Custom HTML layout
    dash_app.index_string = html_layout

    tabs= ['tab1','tab2']

    dash_app.layout = \
        html.Div([
            dcc.Tabs(
                    [dcc.Tab(
                        label=tab,
                        children =
                        html.Div(
                            [table.layout for table in tables if table.data.tab == tab]
                        )
                    ) for tab in tabs]
            ),

            # this below is the div for the plots. It is assigned to both Tabs unless stated otherwise
            html.Div(id = 'graph-container'),
            dcc.Interval(
                id='track-interval',
                interval=ms_interval,  # in milliseconds,
                n_intervals=0
            ),
            store.layout
        ], id='dash-container', className='row')

    results, read_time_list = FirestoreListener(collection_name='karelDB')

    init_callbacks(dash_app, results, tables, table_metrics, store)

    return dash_app.server


def init_callbacks(dash_app, results, tables, table_metrics, store):

    @dash_app.callback(
        store.output('intermediate-data'),
        [Input('track-interval', 'n_intervals')]
    )

    # query data has to be rewritten. no point in creating a df just to feed into the datamaker

    def query_data(n_intervals):

        df_raw = pd.DataFrame(CreateTable(['userId', 'data','date', 'type', 'currentView','item'], results))

        if len(df_raw) == 0:
            return dash.no_update
        else:
            # this could then be added to a dict of dicts eg. level 1 key tab, level 2 key table in tab
            df= IntermediateDataMaker(df_raw, table_metrics)

            return json.dumps(df)

    for table in tables:
        table.callbacks(store.input('intermediate-data'))

    @dash_app.callback(
        Output('graph-container', 'children'),
        [store.input('intermediate-data')]
    )
    def update_table(dfs):

        if dfs is None:
            return dash.no_update
        else:
            datasets = json.loads(dfs)

            value = "attempts"

            df = pd.read_json(datasets[value], orient='split')

            colors = ['#0074D9' for i in range(len(df))]

            # make columns selectable
            # number of actions before completions, times it saw example?

            graph = [html.Div(dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": df["userId"],
                            "y": df[column],
                            "type": "bar",
                            "marker": {"color": colors},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True,
                                  'tickangle': -90},
                        "yaxis": {
                            "automargin": True
                        },
                        "height": 350,
                        # 'paper_bgcolor' : 'rgba(103,128,159,0.5)',
                        'plot_bgcolor': 'rgba(171, 183, 183, 0.2)',
                        "margin": {"t": 30, "l": 10, "r": 10},
                        "title": {
                            'text': column,
                            'y': 0.97,
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'}
                    },
                },
            ),
                className='three columns'
            )
                for column in df.columns[1:]]

            return graph

