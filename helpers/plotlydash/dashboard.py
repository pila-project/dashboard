# -*- coding: utf-8 -*-

"""Instantiate a Dash app."""
#''#158f5e #6eb08c, #b0d0bd, #f1f1f1, #f3baba, #ec8386, #de4355
#old rgba(60,179,113,.5),  rgba(240, 128, 128, .5)
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
from .filemanager import FirestoreListener, DataBars, MaxValueTableStyler, ResultsDataMaker, ReadFirestoreCollection
from google.cloud import firestore
from collections import Counter
from .tabs import Table

import json
import dash_building_blocks as dbb
import time

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

    ms_interval = 3 * 1000

    options = []
    [options.append({'label': k, 'value': k}) for k in dropdown_dict]

    dash_app.index_string = html_layout

    dash_app.layout = \
        html.Div([
            dcc.Tabs(
                parent_className='row',
                className='row',
                #style={'width': '100%'},
                children = [dcc.Tab(
                    # style={'width': '100%'},
                        label='User View',
                        children =
                        html.Div(
                            [
                                html.Div(children=[
                                                   html.Div(children=dcc.Dropdown(id='dropdown-group', options=options,
                                             placeholder='Select...', value='Prolific Jan2021'),style={'display': 'inline-block','vertical-align': 'top','width':'30%',
                                                            'margin-top': '15px','margin-right': '15px','margin-bottom': '15px'}),
                                                   html.Div(children=dcc.Dropdown(id='dropdown-user', placeholder='Select...'),
                                                            style={'display': 'inline-block', 'vertical-align': 'top',
                                                                   'width': '30%', 'margin-bottom': '15px', 'margin-right': '25px', 'margin-top':'15px'}),
                                    html.Div(id='loader-text1',
                                             style={'display': 'inline-block', 'vertical-align': 'top', 'font':'30px Arial',
                                                    'width': '30%', 'margin-bottom': '15px', 'margin-top': '15px'})
                                                   ], style = {'width':'100%'}
                                         ),
                                dash_table.DataTable(
                                    id='data-table1',
                                    page_action="native",
                                    page_size=10,
                                    style_data={'width': '100px'},
                                    style_cell_conditional=[{'if': {'column_id': 'userId'},'width': '250px'},{'if': {'column_id': 'success_emoji'},'width': '30px'}],
                                    style_table={'overflowX': 'auto'},
                                    columns = [{"name": i.capitalize(), "id": i} for i in ['item' ,'avg_n_successes','success_emoji','n_actions', 'n_attempts',
                                                                              'timeto_first_action', 'timeto_success']],
                                    # style_data_conditional=
                                ),
                                html.Div(children='''Legend: Purple background corresponds to a value higher than the reference group, orange background to a lower value. \n
                                Transparent background to a value in line with the reference group ''')
                            ]
                        )),
                        dcc.Tab(label='Glance view',
                                style={'margin':'10px'},
                                children = html.Div([
                                    html.Div([
                                        html.Div(children=dcc.Dropdown(id='dropdown-group2', options=options,
                                                                       placeholder='Select...',
                                                                       value='Prolific Jan2021'),
                                                 style={'display': 'inline-block', 'vertical-align': 'top','margin-top': '15px',
                                                        'margin-bottom': '15px', 'margin-right': '15px', 'width': '30%'}),
                                        html.Div(id='loader-text2',
                                                 style={'display': 'inline-block', 'vertical-align': 'top',
                                                        'font': '30px Arial',
                                                        'width': '30%', 'margin-bottom': '15px', 'margin-top': '15px'})
                                    ], style = {'width':'100%'}),

                                    dash_table.DataTable(
                                        id='data-table2',
                                        page_action="native",
                                        page_size=100,
                                        style_data={'width': '100px'},
                                        style_cell_conditional=[{'if': {'column_id': 'userId'},'width': '250px'}],
                                        style_table={'overflowX': 'auto'},
                                        columns = [{"name": i.capitalize(), "id": i} for i in ['sessionId','userId','Basic Commands', 'Function', 'Repeat' ,'Combine','Challenge']],
                                        style_data_conditional=[
                                            {'if':{'column_id':'Basic Commands','filter_query': '{Basic Commands} eq "True"'},'backgroundColor': '#6eb08c', 'color': 'transparent'},
                                            {'if': {'column_id': 'Basic Commands',
                                                    'filter_query': '{Basic Commands} eq "False"'},
                                             'backgroundColor': '#ec8386', 'color': 'transparent'},
                                            {'if': {'column_id': 'Function',
                                                    'filter_query': '{Function} eq "True"'},
                                             'backgroundColor': '#6eb08c', 'color': 'transparent'},
                                            {'if': {'column_id': 'Function',
                                                    'filter_query': '{Function} eq "False"'},
                                             'backgroundColor': '#ec8386', 'color': 'transparent'},
                                            {'if': {'column_id': 'Repeat',
                                                    'filter_query': '{Repeat} eq "True"'},
                                             'backgroundColor': '#6eb08c', 'color': 'transparent'},
                                            {'if': {'column_id': 'Repeat',
                                                    'filter_query': '{Repeat} eq "False"'},
                                             'backgroundColor': '#ec8386', 'color': 'transparent'},
                                            {'if': {'column_id': 'Combine',
                                                    'filter_query': '{Combine} eq "True"'},
                                             'backgroundColor': '#6eb08c', 'color': 'transparent'},
                                            {'if': {'column_id': 'Combine',
                                                    'filter_query': '{Combine} eq "False"'},
                                             'backgroundColor': '#ec8386', 'color': 'transparent'},
                                            {'if': {'column_id': 'Challenge',
                                                    'filter_query': '{Challenge} eq "True"'},
                                             'backgroundColor': '#6eb08c', 'color': 'transparent'},
                                            {'if': {'column_id': 'Challenge',
                                                    'filter_query': '{Challenge} eq "False"'},
                                             'backgroundColor': '#ec8386', 'color': 'transparent'}
                                        ]
                                    )
                                                     ]
                                )
                        )
                    ]
            ),

            dcc.Interval(
                id='track-interval',
                interval=ms_interval,  # in milliseconds,
                n_intervals=0
            ),

            html.Div(id='data-container', style={'display': 'none'})

        ], id='dash-container', style = {'width':'100%','margin':'20px'}, className='row')

    raw_data_list, read_time_list = FirestoreListener(collection_name='karelDB')

    #raw_data_list = ReadFirestoreCollection(db_name='karelDB')

    init_callbacks(dash_app, raw_data_list, dropdown_dict)

    return dash_app.server


def init_callbacks(dash_app, raw_data_list, dropdown_dict):

    @dash_app.callback(
        Output('data-container','children'),
        [Input('track-interval', 'n_intervals')]
    )
    def query_data(n_intervals):
        if len(raw_data_list) == 0:
            return dash.no_update
        else:
            df = pd.DataFrame.from_records(raw_data_list)

            # formatting and sorting by date
            df['date'] = pd.to_datetime(df.date, format='%Y-%m-%dT%H:%M:%S.%fZ')
            df.sort_values(by='date', inplace=True)

            # Prolific length 15764
            df['sessionId'] = np.where(
                (df.date > '2021-01-08') & (df.userId.astype(str).str.contains('-') == False) & (
                            df.userId.astype(str).str.len() > 20),
                'Prolific Jan2021', 'Other')

            user_df, avg_df = ResultsDataMaker(df)

            print("Data ready with shapes {},{}....".format(user_df.shape, avg_df.shape))
            return json.dumps({'user':user_df.to_json(),'avg':avg_df.to_json()})

    @dash_app.callback(
        Output('dropdown-user','options'),
        [Input('dropdown-group', 'value')]
    )
    def dropdown_data(value):
        options = []
        [options.append({'label': v, 'value': v}) for v in dropdown_dict[value]]

        return options


    @dash_app.callback(
        [Output('data-table1', 'data'),Output('data-table1','style_data_conditional'),Output('loader-text1', 'children')],
        [Input('dropdown-user', 'value'),Input('data-container','children')]
    )
    def update_output(value, dfs):
        try:

            ds = json.loads(dfs) #⭐
            user_df = pd.read_json(ds['user'], orient='records')
            avg_df =  pd.read_json(ds['avg'], orient='records')

            beast = pd.merge(user_df, avg_df, on=['sessionId', 'item'], validate="many_to_one")
            print('Loaded...')

            # n_actions
            beast['n_actions_fmt'] = np.where(beast['n_actions'] > beast['avg_n_actions'] * 1.5, 1, 0)
            beast['n_actions_fmt'] = np.where(beast['n_actions'] < beast['avg_n_actions'] * .5, -1,
                                              beast['n_actions_fmt'])
            # n_attempts
            beast['n_attempts_fmt'] = np.where(beast['n_attempts'] > beast['avg_n_attempts'] * 2, 1, 0)
            beast['n_attempts_fmt'] = np.where(beast['n_attempts'] < beast['avg_n_attempts'] * .5, -1,
                                               beast['n_attempts_fmt'])

            style_data_conditional = DataBars(beast, 'avg_n_successes')
            #style_data_conditional = []

            beast['avg_n_successes'] = beast['avg_n_successes'].values.round(1)

            beast = beast.astype('str')
            beast['success_emoji'] = beast['success'].apply(lambda x: '✅' if x == 'True' else '⭕')

            style_data_conditional += [
                                        {'if': {'column_id': 'n_actions', 'filter_query': '{n_actions_fmt} eq "1"'},
                                         'backgroundColor': 'rgb(160,81,149,0.5)'},
                                        {'if': {'column_id': 'n_actions',
                                                'filter_query': '{n_actions_fmt} eq "-1"'},
                                         'backgroundColor': 'rgba(255,166,0,0.5)'},  # 'color': 'transparent'
                                        {'if': {'column_id': 'n_attempts',
                                                'filter_query': '{n_attempts_fmt} eq "1"'},
                                         'backgroundColor': 'rgb(160,81,149,0.5)'},
                                        {'if': {'column_id': 'n_attempts',
                                                'filter_query': '{n_attempts_fmt} eq "-1"'},
                                         'backgroundColor': 'rgba(255,166,0,0.5)'},
                                        {'if': {'column_id': 'timeto_first_action',
                                                'filter_query': '{timeto_first_action} > {avg_timeto_first_action}'},
                                         'backgroundColor': 'rgb(160,81,149,0.5)'},
                                        {'if': {'column_id': 'timeto_first_action',
                                                'filter_query': '{timeto_first_action} < {avg_timeto_first_action}'},
                                         'backgroundColor': 'rgba(255,166,0,0.5)'},
                                        {'if': {'column_id': 'timeto_success',
                                                'filter_query': '{timeto_success} > {avg_timeto_success}'},
                                         'backgroundColor': 'rgb(160,81,149,0.5)'},
                                        {'if': {'column_id': 'timeto_success',
                                                'filter_query': '{timeto_success} < {avg_timeto_success}'},
                                         'backgroundColor': 'rgba(255,166,0,0.5)'},
                                        {
                                            'if': {'column_id': 'avg_n_successes'},
                                            'color': 'transparent'},
                                    ]
            children_text = '''🎉'''
            return beast.loc[beast.userId == value].to_dict('records'), style_data_conditional, children_text

        except TypeError as e:
            #print(e)
            children_text = '''⏳'''
            return dash.no_update, dash.no_update, children_text

    @dash_app.callback(
        [Output('data-table2', 'data'),Output('loader-text2', 'children')],
        [Input('dropdown-group2', 'value'), Input('data-container', 'children')]
    )
    def update_output(value, dfs):
        try:

            ds = json.loads(dfs)  # ⭐
            user_df = pd.read_json(ds['user'], orient='records')

            pivot_df = user_df.pivot(index='userId', columns='item', values='success')
            pivot_df = pd.merge(pivot_df, user_df[['userId', 'sessionId']].drop_duplicates(), how='left', on='userId', validate='many_to_one')

            pivot_df.fillna(False, inplace=True)
            pivot_df = pivot_df.astype('str')
            print("Ready to display table 2...")
            children_text = '''🎉'''
            return pivot_df.loc[pivot_df.sessionId==value].to_dict('records'), children_text

        except TypeError as e:
            # print(e)
            children_text = '''⏳'''
            return dash.no_update, children_text


dropdown_dict= {
    'Prolific Jan2021':['5d694784be10f9001511d7a3','5ca8c84e92fdc200129e9db3','5f512f610a752a32cf96d74f','5e4c214a69cc03000caf6259',
'5eda126ec6a418029cb19e91','5c44ad201ddd660001ca00b0','5ed1717c9654ab0b17be2ceb','5f043ab655b1f267b94176b4','5fc8d1b43e9eb32a22d4da4d',
'5fc3df4c86fa277559d373c2','5f4bdd0445dcf109c307b90d','5f248b7b1bde03086270bd37','5c102d91e32f860001651a93','5ec970f3e657d60c8e4db3a4',
'5c28efb626e55d0001a685b1','5cfd119645e1a20001883ee6','5fc0c541c266bd597b286e98','5dde8068332b34dd9047e51b','5fa2be9d820efd4e33eee9fc',
'5eedb69308f7161ee954279d','5c7fb04093cdce00160adf49','5b80b3ba16aa4400016a75ef','5fdde74bfdb6e64c26da591a','5efb2cae4187a504713a4081',
'5f9bdffe42555942fbc9ca49','5de631043cf27959fe70269c','5b914a5f02a76000015c72d4','5f2ab8c4c46fc63609d8eedb','5bc2e0ec4f3bfd00012e97b5',
'5e444fa46bcdba04dcf2d695','5dd5105a82569a4c04723f7e','5daec370e4688e00142ca236'],
'Other' : ['bachbumbeng','test','pietro','badabum','bach','test2812v2','badabun','6fe480b2-3373-453f-a0f0-158fd6488325',
'bf87b04d-44e0-4b95-8a58-9b82dcc7cac3','6d82ef11-1627-4c55-a55f-b6d3bd44aeda','mario2','test0401','waseliwas','chidera933',
'2bb6971a-663e-4d68-a5e4-2b440468d3f1','5e9b725d85157c0816f1f0dd','5f908c63832d32168d6d8f31','5d4957bc034616000180b907','5fe8d26e88f0577d2608884f',
'5d78647e4dadc9001a3e34dd','5fe7673ee14422582703e754','test0701','bf15a82f-0abc-4315-b134-8e96714213cb','368a7dbe-f68e-4ed7-845b-4aa3d86bfb06',
'3389c152-52fb-43f5-9589-7634bd5255e1','fab44415-4ddb-41ef-b097-f8e5e38b8fb5','72319cf4-02c6-42d3-8a2f-0f681a52d729','17fb3110-c7b3-4617-b745-d5b0188af829',
'testthis','171d06ba-d8da-45f5-8772-9ec1a2d48cc5','7e3e4436-27ed-4029-8c9c-1e0c0ef57dfe','47a8f09b-c74c-4d57-a382-9bdcca962df7','0a3319ad-d4bb-4a12-8056-afc90a665fb1',
'55ce2fe6-cc03-4904-9ed5-68b0d742fef8','7b97505d-dae7-42f8-99ed-71cf74623e7c','3fc83c8d-838f-454a-bee5-da04204f8dab','900dc138-5c1c-4de9-8876-19e8cfbb26b6',
'81dbc9ba-cc5c-4549-b05a-c35d57735b82','1c36a7e1-b364-4c6f-bffe-8b72e6faa94f','729e1a78-8aba-405f-917a-d9ee92cc62d5','0f78bf68-90f6-40c3-8321-4d64120ea855',
'db0d8681-8bf0-4ae4-b964-12d8172bdbeb','e55b1bcf-8c14-4d7b-a47a-309e09f9deaf','4f667a81-0d8c-4613-9fad-52509de65671']
}