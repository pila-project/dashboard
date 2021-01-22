import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from .layout import html_layout
import plotly.express as px
import datetime, time
from .filemanager import FirestoreListener, ResultsDataMaker
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
                html.H1("{}".format(self.data.name), style={'padding-bottom':'10px', 'color':'rgba(46, 49, 49, 1)'}),
                dcc.Dropdown(id=self.register('dropdown-menu'), options = self.data.options, placeholder='Select...'),
                dash_table.DataTable(
                    id=self.register('data-table'), #self register == global table names like 'data-table-{}'.format(self.data.name)
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

    def callbacks(self, intermediate_input, time_interval):
        @self.app.callback(
            [
                self.output('data-table', 'data'),
                self.output('data-table', 'columns')
            ],
            [intermediate_input, time_interval]
        )
        def update_table(data_list, time_interval):
            columns = [{"name": i, "id": i} for i in ['userId','sessionId', 'item', 'actions', 'attempts', 'success', 'time_success',
       'time_first', 'timedout', 'examples']]

            print("data", data_list)

            return data_list, columns
            # try:
            #     df = pd.DataFrame(data_list,
            #                       columns=['userId', 'sessionId',
            #                                'item', 'actions',
            #                                'attempts', 'success',
            #                                'time_success','time_first',
            #                                'timedout','examples'])
            #
            #     data = df.to_dict('records')
            #     columns = [{"name": i, "id": i, "selectable": True} for i in df.columns]
            #     # print("dropdown col is {}".format(self.data.dropdown_col))
            #     print("Data length is {}".format(len(data)))
            #     return data, columns
            #
            # except ValueError as e:
            #     print(e)
            #     return dash.no_update


# try with one table identical but not defined through dbb
