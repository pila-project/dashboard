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
from .filemanager import FirestoreListener, CreateTable, IndexFlattener, DataBars, MaxValueTableStyler
from google.cloud import firestore
from collections import Counter



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

    ms_interval = 60 * 1000

    # Custom HTML layout
    dash_app.index_string = html_layout

    table_columns = ['userId','outcome','ModifyMoves', 'CommandsMLMR','KarelDrifts', 'KarelMoves']
    opts = [{'label': i, 'value': i} for i in table_columns]

    table_metrics = ['attempts','successes']
    metrics = [{'label': i.capitalize(), 'value':i} for i in table_metrics]

    dash_app.layout = \
        html.Div([
        dcc.Tabs([
                     dcc.Tab(label="Tab one", children=[
                                                                 html.Div([
                                                                     html.Label("Select currentView of interest"),
                                                                     dcc.Dropdown(id='opt',
                                                                                  options=opts,
                                                                                  value=table_columns,
                                                                     multi = True)], style = {'fontSize':'20px','color':'#808080','display': 'inline-block','padding-top': '20px'}, className='four columns'),
                         html.Div([
                             dash_table.DataTable(
                                 id='data-table',
                                 row_selectable='multi',
                                 selected_rows= [],
                                 column_selectable = 'multi',
                                 selected_columns=[],
                                 sort_action="native",
                                 sort_mode='native',
                                 page_size=300,
                                 style_cell={'textAlign': 'left'},
                                 style_header={
                                     'backgroundColor': 'rgb(230, 230, 230)',
                                     'fontWeight': 'bold'
                                 }
                             )
                         ],style={'padding-top': '20px'}, className='eight columns')
                        ]),
                dcc.Tab(label="Tab two",children=[   html.Div([
                             dash_table.DataTable(
                                 id='data-table2',
                                 sort_action="native",
                                 sort_mode='native',
                                 page_action = 'native',
                                 page_size=10,
                                style_cell = {'textAlign': 'left'},
                                 style_header={
                                     'border': '1px solid rgb(189,189,210)',
                                     'backgroundColor': 'rgb(230, 230, 230)',
                                     'fontWeight': 'bold'})
                         ], style={'padding-top': '20px'}, className='four columns'),
                html.Div([dcc.Graph(
                    id='bar-graph')],style={'padding-top': '20px'}, className='eight columns')]),
                dcc.Tab(label="Tab three", children = html.Div([html.Div(html.H1("Select metric of interest"),style={'padding-top': '20px'}),
                                                                     html.Div(dcc.Dropdown(
                                                                         id='opt-3',
                                                                                  options= metrics,
                                                                                  value=table_metrics[0],
                                                                                  multi = False),
                                                                     style={'padding-bottom': '20px', 'padding-top': '10px'}),
                                                                html.Div(dash_table.DataTable(
                    id='data-table3',
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    selected_rows=[],
                    page_action="native",
                    page_size=10)),
                    html.Div(id = 'graph-container')
                                                                ])
                        )
        ]),
            dcc.Interval(
                id='track-interval',
                interval=ms_interval,  # in milliseconds,
                n_intervals=0)
        ], id='dash-container', className='row')

    results, read_time_list = FirestoreListener(collection_name='karelDB')

    init_callbacks(dash_app, results, read_time_list, ms_interval)

    return dash_app.server



def init_callbacks(dash_app, results, read_time_list, ms_interval):


    #tab3
    @dash_app.callback(
        [
            Output('graph-container','children'),
         Output('data-table3','columns'),
         Output('data-table3','data'),
         ],
        [Input('track-interval', 'n_intervals'),
         Input('data-table3', 'selected_rows'),
         Input('opt-3', 'value')
         ]
    )
    def update_graphseries(rows,
                           user_selected_rows,
                           value
                           ):

        if user_selected_rows is None:
            user_selected_rows = []

        df_tab3 = pd.DataFrame(CreateTable(['userId', 'data', 'type', 'currentView'], results))

        dic_tab3 = {}

        col = value

        if col == 'attempts':
            cond = (df_tab3.type.str.startswith("RUN_DONE"))
        else:
            cond = (df_tab3.type.str.startswith("RUN_DONE"))&(df_tab3.data.str.startswith('successful'))

        dic_tab3[col] = pd.DataFrame(df_tab3[
            cond].groupby(
            ['userId', 'currentView']).count()['data'])

        dic_tab3[col] = pd.pivot_table(dic_tab3[col], index=['userId'], columns='currentView').fillna(
    0).reset_index()

        dic_tab3[col][dic_tab3[col].columns[1:]] = dic_tab3[col][dic_tab3[col].columns[1:]].astype('int')

        dic_tab3[col] = IndexFlattener(dic_tab3[col])


        colors = ['#7FDBFF' if i in user_selected_rows else '#0074D9'
                   for i in range(len(dic_tab3[col]))]

        data = dic_tab3[col].to_dict('records')
        columns = [{"name": i, "id": i, "selectable": True} for i in dic_tab3[col].columns]

        #make columns selectable
        #number of actions before completions, times it saw example?

        graph = [html.Div(dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": dic_tab3[col]["userId"],
                            "y": dic_tab3[col][column],
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
                        #'paper_bgcolor' : 'rgba(103,128,159,0.5)',
                        'plot_bgcolor' : 'rgba(171, 183, 183, 0.2)',
                        "margin": {"t":30, "l": 10, "r": 10},
                        "title": {
        'text': column,
        'y': 0.97,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
                    },
                },
            ),
            className= 'three columns'
        )
            for column in dic_tab3[col].columns[1:]]

        return graph, columns, data




    #tab1
    @dash_app.callback(
        [Output('data-table','data'), Output('data-table','columns'), Output('data-table','style_data_conditional')],
        [Input('track-interval', 'n_intervals'),Input('opt', 'value'),Input('data-table', 'selected_rows'), Input('data-table', 'selected_columns')]
    )
    def update_tables(rows, values, user_selected_rows, user_selected_columns):

        #df = CreateTable('data', results)
        if (read_time_list[-1].timestamp() * 1000 < datetime.datetime.utcnow().timestamp() * 1000 - ms_interval):

            print('nothing has changed between {} and now {}'.format(read_time_list[-1], datetime.datetime.utcnow()))
            try:
                df_tab1
            except NameError:
                print('df doesn\'t exist')
                df_tab1 = pd.DataFrame(CreateTable(['userId', 'data', 'type', 'currentView'], results))

                df_tab1 = pd.DataFrame(
                    df_tab1[(df_tab1.type.str.startswith("RUN_DONE"))].groupby(['userId', 'currentView'])['data'].value_counts() /
                    df_tab1[
                        (df_tab1.type.str.startswith("RUN_DONE"))].groupby(['userId', 'currentView'])[
                        'data'].count() * 100).rename(columns={'data': 'frequency'}).reset_index()

                df_tab1 = pd.pivot_table(df_tab1, index=['userId', 'data'], columns='currentView').fillna(0).reset_index().rename(
                    columns={'data': 'outcome'})

                df_tab1 = IndexFlattener(df_tab1)
            else:
                print('df exists')
                pass
        else:
            print('something has changed between {} and now {}'.format(read_time_list[-1], datetime.datetime.utcnow()))

            df_tab1 = pd.DataFrame(CreateTable(['userId', 'data', 'type', 'currentView'], results))

            df_tab1 = pd.DataFrame(
                df_tab1[(df_tab1.type.str.startswith("RUN_DONE"))].groupby(['userId', 'currentView'])['data'].value_counts() / df_tab1[
                    (df_tab1.type.str.startswith("RUN_DONE"))].groupby(['userId', 'currentView'])[
                    'data'].count() * 100).rename(columns={'data': 'frequency'}).reset_index()

            df_tab1 = pd.pivot_table(df_tab1, index=['userId', 'data'], columns='currentView').fillna(0).reset_index().rename(
                columns={'data': 'outcome'})

            df_tab1 = IndexFlattener(df_tab1)



        #filter rows based on selected_rows
        if user_selected_rows is None:
            print('row list is empty')
            user_selected_rows = []
        elif len(user_selected_rows) != 0:
            [print(row) for row in user_selected_rows]
            df_tab1 = df_tab1.iloc[user_selected_rows]
        else:
            pass



        # filter out currentview based on dropdown
        df_tab1 = df_tab1[values].round(1)

        # filter columns based on selected_columns
        if user_selected_columns is None:
            print('col list is empty')
            user_selected_columns = []
        elif len(user_selected_columns) != 0:
            [print(col) for col in user_selected_columns]
            # df_tab1 = df_tab1[user_selected_columns]
        else:
            pass

        data = df_tab1.to_dict('records')

        columns = [{"name": i, "id": i, "selectable": True} for i in df_tab1.columns]



        style_data_conditional = MaxValueTableStyler(df_tab1)
        style_data_list = []
        for val in values:

            if (val == "userId") or (val == "outcome"):
                pass
            else:
                #print("{} added to style list".format(val))
                style_data_list.extend(DataBars(df_tab1,val))

        style_data_conditional =style_data_list

        return data, columns, style_data_conditional

    #tab2
    @dash_app.callback(
        [Output('bar-graph', 'figure'), Output('data-table2','data'), Output('data-table2','columns') ],
        [Input('track-interval', 'n_intervals')]
    )
    def update_graphs(rows):
        #if latest readtime different from current, update. how about first caase?
        #if latest_read_time
        if (read_time_list[-1].timestamp() * 1000 < datetime.datetime.utcnow().timestamp() * 1000 - ms_interval):

            print('nothing has changed between {} and now {}'.format(read_time_list[-1], datetime.datetime.utcnow()))
            try:
                df_tab2
            except NameError:
                print('df doesn\'t exist')
                counter = Counter(CreateTable(['data'], results)['data'])
                df_tab2 = pd.DataFrame(list(counter.items()), columns=['Action', 'Count']).sort_values('Count',ascending=False)
                df_tab2 = df_tab2[~(df_tab2.Action.str.contains("xml"))]

            else:
                print('df exists')
                pass
        else:
            print('something has changed between {} and now {}'.format(read_time_list[-1],datetime.datetime.utcnow()))
            counter = Counter(CreateTable(['data'], results)['data'])
            df_tab2 = pd.DataFrame(list(counter.items()), columns=['Action', 'Count']).sort_values('Count',ascending=False)
            df_tab2 = df_tab2[~(df_tab2.Action.str.contains("xml"))]


        fig = px.bar(df_tab2, x='Action', y='Count', opacity = 0.6)

        # Customize aspect
        fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6)

        fig.update_layout(title_text='Count of user action as of {}'.format(datetime.datetime.utcnow().strftime("%Y-%m-%d, %H:%M:%S")))


        data = df_tab2.to_dict('records')

        columns = [{"name": i, "id": i} for i in df_tab2.columns]

        return fig, data, columns





#last working version
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

    # Custom HTML layout
    dash_app.index_string = html_layout

    table_columns = ['userId','outcome','ModifyMoves', 'CommandsMLMR','KarelDrifts', 'KarelMoves']
    opts = [{'label': i, 'value': i} for i in table_columns]

    table_metrics = ['attempts']
    metrics = [{'label': i.capitalize(), 'value':i} for i in table_metrics]

    dash_app.layout = \
        html.Div([
            dcc.Tabs([
                dcc.Tab(label="Tab three",
                        children = html.Div(
                            [
                                html.Div(
                                    dash_table.DataTable(
                                        id='data-table3',
                                        filter_action="native",
                                        sort_action="native",
                                        sort_mode="multi",
                                        page_action="native",
                                        page_size=10
                                    )
                                ),
                        # this below is the div for the plots
                        html.Div(id = 'graph-container')
                            ]
                        )
                        )
            ]),
            dcc.Interval(
                id='track-interval',
                interval=ms_interval,  # in milliseconds,
                n_intervals=0
            ),
            html.Div(id='intermediate-value', style={'display': 'none'})
        ], id='dash-container', className='row')

    results, read_time_list = FirestoreListener(collection_name='karelDB')

    init_callbacks(dash_app, results, read_time_list, ms_interval, table_metrics)

    return dash_app.server


def init_callbacks(dash_app, results, read_time_list, ms_interval, table_metrics):

    @dash_app.callback(
        Output('intermediate-value', 'children'),
        [Input('track-interval', 'n_intervals')]
    )
    def query_data(n_intervals):

        df_raw = pd.DataFrame(CreateTable(['userId', 'data', 'type', 'currentView'], results))

        if len(df_raw) == 0:
            return dash.no_update
        else:
            dic_tab3 = {}

            cond = (df_raw.type.str.startswith("RUN_DONE")) # & (df_tab3.data.str.startswith('successful'))

            df_grouped = pd.DataFrame(
                df_raw[cond].groupby(
                    ['userId', 'currentView']).count()['data']
            )

            col = table_metrics[0]

            dic_tab3[col] = pd.pivot_table(df_grouped, index=['userId'], columns='currentView').fillna(
                0).reset_index()

            #formatting int
            dic_tab3[col][dic_tab3[col].columns[1:]] = dic_tab3[col][dic_tab3[col].columns[1:]].astype('int')

            dic_tab3[col] = IndexFlattener(dic_tab3[col])

            #this could become a dict of dict eg. level 1 key tab, level 2 key table in tab
            dic_tab3[col] =  dic_tab3[col].to_json(orient='split', date_format='iso')
            return json.dumps(dic_tab3)

    @dash_app.callback(
        [
            Output('data-table3', 'data'),
            Output('data-table3', 'columns')
         ],
        [Input('intermediate-value', 'children')]
    )
    def update_table(dfs):

        if dfs is None:
            return dash.no_update
        else:
            datasets = json.loads(dfs)

            value = table_metrics[0]

            dic_tab3 = pd.read_json(datasets[value], orient='split')

            colors = ['#0074D9' for i in range(len(dic_tab3))]

            data = dic_tab3.to_dict('records')
            columns = [{"name": i, "id": i, "selectable": True} for i in dic_tab3.columns]

            #make columns selectable
            #number of actions before completions, times it saw example?

            graph = [html.Div(dcc.Graph(
                    id=column,
                    figure={
                        "data": [
                            {
                                "x": dic_tab3["userId"],
                                "y": dic_tab3[column],
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
                            #'paper_bgcolor' : 'rgba(103,128,159,0.5)',
                            'plot_bgcolor' : 'rgba(171, 183, 183, 0.2)',
                            "margin": {"t":30, "l": 10, "r": 10},
                            "title": {
            'text': column,
            'y': 0.97,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
                        },
                    },
                ),
                className= 'three columns'
            )
                for column in dic_tab3.columns[1:]]

            return data, columns

