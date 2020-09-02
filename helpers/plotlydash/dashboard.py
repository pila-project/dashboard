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
from .filemanager import FirestoreListener, CreateTable
from google.cloud import firestore
from collections import Counter



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

    ms_interval = 5 * 1000

    # Custom HTML layout
    dash_app.index_string = html_layout

    dash_app.layout = html.Div(
        children=[
            dcc.Graph(
            id='bar-graph'),

            #html.H1('The time is: ' + str(datetime.datetime.now())),

            dash_table.DataTable(
                id='data-table',
                sort_action="native",
                sort_mode='native',
                page_size=300),

            dcc.Interval(
            id = 'track-interval',
                interval = ms_interval,  # in milliseconds,
                n_intervals = 0),
        ],
        id='dash-container'
    )

    results, read_time_list = FirestoreListener(collection_name='karelDB')

    init_callbacks(dash_app, results, read_time_list, ms_interval)

    return dash_app.server



def init_callbacks(dash_app, results, read_time_list, ms_interval):
    @dash_app.callback(
        [Output('bar-graph', 'figure'), Output('data-table','data'), Output('data-table','columns') ],
        [Input('track-interval', 'n_intervals')]
    )
    def update_graphs(rows):
        #if latest readtime different from current, update. how about first caase?
        #if latest_read_time
        if (read_time_list[-1].timestamp() * 1000 < datetime.datetime.now().timestamp() * 1000 - ms_interval*2):

            print('nothing has changed between {} and now {}'.format(read_time_list[-1], datetime.datetime.utcnow()))
            try:
                df
            except NameError:
                print('df doesn\'t exist')
                counter = Counter(CreateTable('data', results))
                df = pd.DataFrame(list(counter.items()), columns=['Action', 'Count']).sort_values('Count',ascending=False)
                df = df[~(df.Action.str.contains("xml"))]

            else:
                print('df exists')
                pass
        else:
            print('something has changed between {} and now {}'.format(read_time_list[-1],datetime.datetime.utcnow()))
            counter = Counter(CreateTable('data', results))
            df = pd.DataFrame(list(counter.items()), columns=['Action', 'Count']).sort_values('Count',ascending=False)
            df = df[~(df.Action.str.contains("xml"))]


        fig = px.bar(df, x='Action', y='Count', opacity = 0.6)

        # Customize aspect
        fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6)

        fig.update_layout(title_text='Count of user action as of {}'.format(datetime.datetime.utcnow().strftime("%Y-%m-%d, %H:%M:%S")))


        data = df.to_dict('records')

        columns = [{"name": i, "id": i} for i in df.columns]

        return fig, data, columns







