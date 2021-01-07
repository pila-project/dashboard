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
from .filemanager import FirestoreListener, CreateTable, IndexFlattener, DataBars, MaxValueTableStyler
from google.cloud import firestore
from collections import Counter

import json
import dash_building_blocks as dbb
#remember to use store
import dash_building_blocks as dbb


class Table(dbb.Block):
    '''
    the data attribute is a 1-level dictionary that contains:
    - name: Table Name
    -


    '''
    def layout(self):
        return html.Div([
                html.H1("Table on metric: {}".format(self.data.name), style={'padding-bottom':'10px', 'color':'rgba(46, 49, 49, 1)'}),
                dash_table.DataTable(
                    id=self.register('data-table'), #self register free us from creating global table names like 'data-table-{}'.format(self.data.name)
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    page_action="native",
                    page_size=10,
                    style_data={
                        'width': '100px',
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'userId'},
                            'width': '250px'
                        },
                    ],
                    style_table={
                        'overflowX': 'auto'
                    }
                )
        ])

    def callbacks(self, intermediate_input):
        @self.app.callback(
            [
                self.output('data-table', 'data'),
                self.output('data-table', 'columns')
            ],
            [intermediate_input]
        )
        def update_table(dfs):

            if dfs is None:
                return dash.no_update
            else:
                datasets = json.loads(dfs)

                df = pd.read_json(datasets[self.data.name], orient='split')

                data = df.to_dict('records')
                columns = [{"name": i, "id": i, "selectable": True} for i in df.columns]

            return data, columns