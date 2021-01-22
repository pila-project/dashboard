#
#
# from collections import Counter
# import pandas as pd
#
# # prolific study user ids
# #
#
# df = pd.DataFrame(CreateTable(['userId', 'data', 'date', 'type', 'currentView', 'item'], raw_data_list))
# df['date'] = pd.to_datetime(df.date, format='%Y-%m-%dT%H:%M:%S.%fZ')
# df.sort_values(by='date', inplace=True)
#
# #PROLIFIC only
# df.loc[(df.date>'2021-01-08')&(df.userId.str.contains('-')==False)&(df.userId.str.len()>20)].userId
#
# item_list = ['Basic Commands','Function','Repeat','Combine','Challenge']
#
# example_dict = {'Basic Commands': ['CommandsHouseGood', 'CommandsHouseBad'],
#                 'Function': ['MethodsTurnAroundBad', "MethodsTurnAroundGood"],
#                 'Repeat': ["RepeatL2StepUpGood", "RepeatL2StepUpBad"],
#                 'Combine': ['RepeatL3Dash5Good', 'RepeatL3Dash5Bad'],
#                 'Challenge': ['DiamondGood', 'DiamondBad']}
#
# # user = '5eb8630fb9a7c17ac8c7d14b'
# # item = 'Function'
#
# data_list = []
#
# ## within-item indicators:
# for user in df.userId.unique():
#
#     for item in item_list:
#
#         #print(user, item)
#
#         #actions (excluding BUTTON_CLICK_run and BUTTON_CLICK_reset)
#         n_actions = Counter(df.loc[(df.item == item) & (df.userId == user)].type)
#         action = n_actions['UPDATE_CODE_move'] + n_actions['UPDATE_CODE_delete']
#
#         #attempts/successes
#         n_runs = Counter(df.loc[(df.item == item) & (df.type == 'RUN_DONE') & (df.userId == user)].data)
#         attempts = n_runs['unsuccessful']
#         success = (n_runs['successful']>0)
#
#         #time
#         try:
#             start = df.loc[(df.currentView == 'dashboard') & (df.item == item) & (df.userId == user)].date.values[0]
#             first = df.loc[(df.item == item) & (df.userId == user)].date.values[3]#first three actions usually same time stamp
#             end = df.loc[(df.data == 'successful') & (df.type == 'RUN_DONE') & (df.item == item) & (
#                         df.userId == user)].date.values[0]
#         except IndexError as e:
#             print("Index Error for user {} in item {}".format(user, item))
#             start = 0
#             first = 0
#             end = 0
#
#         time_success = pd.Timedelta(end - start).total_seconds()
#         time_first = pd.Timedelta(first - start).total_seconds()
#         timedout = (n_actions['TIMEDOUT'] > 0)
#
#         # opened examples
#         examples = (len(df.loc[(df.type == "UPDATE_CURRENT_VIEW") & (df.data.isin(example_dict[item])) & (df.userId == user)].data) > 0)
#
#         #result list
#         data_list.append([user, item, action, attempts, success, time_success, time_first, timedout, examples])
#
# results_df = pd.DataFrame(data_list,
#     columns=['userId', 'item', 'actions', 'attempts', 'success', 'time_success', 'time_first', 'timedout',
#              'examples'])
#
# #
# #
# # ## task-level indicators:
# # gl_start = df.loc[(df.currentView == 'dashboard')].date.values[0]
# # gl_end = df.date.values[-1]
# #
# # # total time spent
# # print(int(pd.Timedelta(gl_end - gl_start).total_seconds() / 60))
# #
# # # total # items completed
# #
# #
# # # total # items opened (update_code>0)
# #
# # # total # items attempted (rundone >0)
# #
# # # total # items timedout
#
#
# # this below is the div for the plots. It is assigned to both Tabs unless stated otherwise
# # html.Div(id = 'graph-container'),
#
# # @dash_app.callback(
# #     Output('graph-container', 'children'),
# #     [store.input('intermediate-data')]
# # )
# # def update_plot(dfs):
# #
# #     if dfs is None:
# #         return dash.no_update
# #     else:
# #         datasets = json.loads(dfs)
# #
# #         value = "attempts"
# #
# #         df = pd.read_json(datasets[value], orient='split')
# #
# #         colors = ['#0074D9' for i in range(len(df))]
# #
# #         # make columns selectable
# #         # number of actions before completions, times it saw example?
# #
# #         graph = [html.Div(dcc.Graph(
# #             id=column,
# #             figure={
# #                 "data": [
# #                     {
# #                         "x": df["userId"],
# #                         "y": df[column],
# #                         "type": "bar",
# #                         "marker": {"color": colors},
# #                     }
# #                 ],
# #                 "layout": {
# #                     "xaxis": {"automargin": True,
# #                               'tickangle': -90},
# #                     "yaxis": {
# #                         "automargin": True
# #                     },
# #                     "height": 350,
# #                     # 'paper_bgcolor' : 'rgba(103,128,159,0.5)',
# #                     'plot_bgcolor': 'rgba(171, 183, 183, 0.2)',
# #                     "margin": {"t": 30, "l": 10, "r": 10},
# #                     "title": {
# #                         'text': column,
# #                         'y': 0.97,
# #                         'x': 0.5,
# #                         'xanchor': 'center',
# #                         'yanchor': 'top'}
# #                 },
# #             },
# #         ),
# #             className='three columns'
# #         )
# #             for column in df.columns[1:]]
# #
# #         return graph
#
#
# # @dash_app.callback(
# #     Output("dropdown-menu", "options"),
# #     [store.input('intermediate-data'), Input('track-interval', 'n_intervals')]
# # )
# # def dropdown(data_list,times):
# #     # try:
# #     #     df = pd.DataFrame(data_list,
# #     #                               columns=['userId', 'item', 'actions', 'attempts', 'success', 'time_success',
# #     #                                        'time_first',
# #     #                                        'timedout',
# #     #                                        'examples'])
# #     #     options =[]
# #     #     [options.append({'label':u,'value':u}) for u in df.userId.unique()]
# #     #     print('we are here')
# #     #     return options
# #     #
# #     # except ValueError as e:
# #     #     # print(e)
# #     #     return dash.no_update
# #     options = [{'label':'1','value':'1'}]
# #     return options
#
# #
# # def ResultsDataMaker(raw_data_list):
# #     '''takes raw_data_list as input and returns results_df'''
# #
# #     df = pd.DataFrame(CreateTable(['userId', 'data', 'date', 'type', 'currentView', 'item'], raw_data_list))
# #
# #     # PROLIFIC only (in a later stage this is the condition to define sessionId value)
# #     df['sessionId'] = np.where(df.loc[(df.date > '2021-01-08') & (df.userId.str.contains('-') == False) & (df.userId.str.len() > 20)],'Prolific Jan2021','Other')
# #
# #     #formatting and sorting by date
# #     df['date'] = pd.to_datetime(df.date, format='%Y-%m-%dT%H:%M:%S.%fZ')
# #     df.sort_values(by='date', inplace=True)
# #
# #     item_list = ['Basic Commands', 'Function', 'Repeat', 'Combine', 'Challenge']
# #
# #     example_dict = {'Basic Commands': ['CommandsHouseGood', 'CommandsHouseBad'],
# #                     'Function': ['MethodsTurnAroundBad', "MethodsTurnAroundGood"],
# #                     'Repeat': ["RepeatL2StepUpGood", "RepeatL2StepUpBad"],
# #                     'Combine': ['RepeatL3Dash5Good', 'RepeatL3Dash5Bad'],
# #                     'Challenge': ['DiamondGood', 'DiamondBad']}
# #
# #     data_list = []
# #     #metrics
# #     metrics = ['actions', 'attempts', 'time_success', 'time_first','timedout', 'examples']
# #
# #     for item in item_list:
# #         print(item)
# #
# #
# #
# #     ## within-item indicators:
# #     for user in df.userId.unique():
# #
# #         for item in item_list:
# #
# #             # actions (excluding BUTTON_CLICK_run and BUTTON_CLICK_reset)
# #             n_actions = Counter(df.loc[(df.item == item) & (df.userId == user)].type)
# #             action = n_actions['UPDATE_CODE_move'] + n_actions['UPDATE_CODE_delete']
# #
# #             # attempts/successes
# #             n_runs = Counter(df.loc[(df.item == item) & (df.type == 'RUN_DONE') & (df.userId == user)].data)
# #             attempts = n_runs['unsuccessful']
# #             success = (n_runs['successful'] > 0)
# #
# #             # time
# #             try:
# #                 start = df.loc[(df.currentView == 'dashboard') & (df.item == item) & (df.userId == user)].date.values[0]
# #                 first = df.loc[(df.item == item) & (df.userId == user)].date.values[3]  # first three actions usually same time stamp
# #                 end = df.loc[(df.data == 'successful') & (df.type == 'RUN_DONE') & (df.item == item) & (
# #                         df.userId == user)].date.values[0]
# #             except IndexError as e:
# #                 #print("Index Error for user {} in item {}".format(user,item))
# #                 start = 0
# #                 first = 0
# #                 end = 0
# #
# #             time_success = strfdelta(pd.Timedelta(end - start).round('S'),"{minutes}:{seconds}")
# #             time_first = strfdelta(pd.Timedelta(first - start).round('S'),"{minutes}:{seconds}")
# #             timedout = (n_actions['TIMEDOUT'] > 0)
# #
# #             # opened examples
# #             examples = (len(df.loc[(df.type == "UPDATE_CURRENT_VIEW") & (df.data.isin(example_dict[item])) & (
# #                         df.userId == user)].data) > 0)
# #
# #             #session
# #             sessionId = df.loc[df.userId==user].sessionId.values[0]
# #
# #             # result list
# #             data_list.append({'userId':user, 'sessionId':sessionId,
# #                                'item':item, 'actions':action,
# #                                'attempts': attempts,'success': success,
# #                                'time_success':time_success,'time_first': time_first,
# #                                'timedout': timedout, 'examples':examples})
# #
# #     return data_list
#
#
# #this is supported natively by pandas.DataFrame.from_records(list)
# # def CreateTable(
# #         key_names: [],
# #         list_dict_name: str
# # ):
# #     table = {}
# #     # add sorting by timestamp
# #     # [table.append(ev.get(key_name)) for key_name in key_names for ev in dict_name]
# #     for key_name in key_names:
# #
# #         table[key_name] = []
# #
# #         for ev in list_dict_name:
# #             table[key_name].append(ev.get(key_name))
# #
# #     return table
# #
# # def strfdelta(tdelta, fmt):
# #     d = {"days": tdelta.days}
# #     d["hours"], rem = divmod(tdelta.seconds, 3600)
# #     d["minutes"], d["seconds"] = divmod(rem, 60)
# #     return fmt.format(**d)
# #
# #
# # def IntermediateDataMaker(df, columns):
# #     '''add descr'''
# #
# #     dic_tab = {}
# #
# #     # cond and groupby could become inputs
# #     cond = (df.type.str.startswith("RUN_DONE"))  # & (df_tab3.data.str.startswith('successful'))
# #
# #     df_grouped = pd.DataFrame(
# #         df[cond].groupby(
# #             ['userId', 'currentView']).count()['data']
# #     )
# #
# #     for col in columns:
# #         dic_tab[col] = pd.pivot_table(df_grouped, index=['userId'], columns='currentView').fillna(
# #             0).reset_index()
# #
# #         # formatting int
# #         dic_tab[col][dic_tab[col].columns[1:]] = dic_tab[col][dic_tab[col].columns[1:]].astype('int')
# #
# #         dic_tab[col] = IndexFlattener(dic_tab[col])
# #
# #         # this could become a dict of dict eg. level 1 key tab, level 2 key table in tab
# #         dic_tab[col] = dic_tab[col].to_json(orient='split', date_format='iso')
# #
# #     return dic_tab
#
#
# # def IndexFlattener(df):
# #     '''add desc'''
# #     for col in df.columns:
# #         if col[1] == '':
# #             pass
# #         else:
# #             df[col[1]] = df[col]
# #             df = df.drop(col, axis=1)
# #
# #     df.columns = df.columns.get_level_values(0)
# #
# #     return df
#
#
# # def ReadFirestoreDocument(doc_name: str, collection_name: str = "karelDB"):
# #
# #     db = firestore.Client.from_service_account_json("keys/pila-277913-44ed571ccec0.json")
# #
# #     doc_ref = db.collection(collection_name).document(doc_name)
# #     doc = doc_ref.get()
# #
# #     return doc.to_dict()
# # def TimeConverter(timecol, fmt="%Y-%m-%dT%H:%M:%S.%fZ"):
# #     '''Converts time feature to a given format'''
# #     return pd.to_datetime(timecol, format=fmt)
#
#
# #this was data.py
# # """Prepare data for Plotly Dash."""
# # import pandas as pd
# # import numpy as np
# #
# # from .filemanager import ReadFirestoreCollection, TimeConverter, CreateTable, FirestoreListener
# # from collections import Counter
# # from google.cloud import firestore
# #
# #
# #
# # def CreateDataFrame(collection_name:str="karelDB"):
# #     results = FirestoreListener(collection_name=collection_name)
# #     print(results)
# #
# #     counter = Counter(CreateTable('data', results))
# #
# #     df = pd.DataFrame(list(counter.items()), columns=['Action', 'Count'])
# #
# #     return df
# #
# #
# # # def CreateDataFrame(collection_name="karelDB"):
# # #
# # #     df=pd.DataFrame{'Action': {0: 'Welcome',
# # #                 1: 'MeetKarel',
# # #                 2: 'KarelCommandsMove',
# # #                 3: 'KarelCommandsTurnLeft',
# # #                 4: 'KarelCommandsPickStone',
# # #                 5: 'KarelCommandsPlaceStone'},
# # #      'Count': {0: 3, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}}
# # #
# # #     return df
# #
#
# df4 = pd.DataFrame([{'userId': '59dbee057f3d71000171d37d', 'sessionId':'Prolific Jan2021', 'item': 'Combine', 'actions': 0, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
# {'userId': '59dbee057f3d71000171d37d', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 0, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
#                         {'userId': '5d694784be10f9001511d7a3', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 25, 'attempts': 1, 'success': True, 'time_success': 44.872, 'time_first': 7.179, 'timedout': False, 'examples': False},
#                         {'userId': '5d694784be10f9001511d7a3', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 8, 'attempts': 0, 'success': True, 'time_success': 54.039, 'time_first': 25.333, 'timedout': False, 'examples': False},
#                         {'userId': '5d694784be10f9001511d7a3', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 72, 'attempts': 3, 'success': True, 'time_success': 240.944, 'time_first': 18.375, 'timedout': False, 'examples': False},
#                         {'userId': '5d694784be10f9001511d7a3', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 32, 'attempts': 0, 'success': True, 'time_success': 155.558, 'time_first': 8.506, 'timedout': False, 'examples': False},
#                         {'userId': '5d694784be10f9001511d7a3', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 300, 'attempts': 2, 'success': True, 'time_success': 851.629, 'time_first': 9.43, 'timedout': False, 'examples': False},
#                         {'userId': '5f512f610a752a32cf96d74f', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 45, 'attempts': 3, 'success': True, 'time_success': 139.408, 'time_first': 17.532, 'timedout': False, 'examples': False},
#                         {'userId': '5f512f610a752a32cf96d74f', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 52, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': True, 'examples': False},
#                         {'userId': '5f512f610a752a32cf96d74f', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 129, 'attempts': 10, 'success': True, 'time_success': 829.119, 'time_first': 28.876, 'timedout': False, 'examples': True},
#                         {'userId': '5f512f610a752a32cf96d74f', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 55, 'attempts': 2, 'success': True, 'time_success': 276.679, 'time_first': 28.731, 'timedout': False, 'examples': False},
#                         {'userId': '5f512f610a752a32cf96d74f', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 321, 'attempts': 2, 'success': True, 'time_success': 907.113, 'time_first': 46.444, 'timedout': False, 'examples': False},
#                         {'userId': '5ca8c84e92fdc200129e9db3', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 21, 'attempts': 7, 'success': True, 'time_success': 99.96, 'time_first': 16.264, 'timedout': False, 'examples': False},
#                         {'userId': '5ca8c84e92fdc200129e9db3', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 40, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': True},
#                         {'userId': '5ca8c84e92fdc200129e9db3', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 0, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
#                         {'userId': '5ca8c84e92fdc200129e9db3', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 0, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
#                         {'userId': '5ca8c84e92fdc200129e9db3', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 0, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
#                         {'userId': '5e4c214a69cc03000caf6259', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 8, 'attempts': 0, 'success': True, 'time_success': 22.742, 'time_first': 11.708, 'timedout': False, 'examples': False},
#                         {'userId': '5e4c214a69cc03000caf6259', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 12, 'attempts': 0, 'success': True, 'time_success': 100.605, 'time_first': 33.335, 'timedout': False, 'examples': False},
#                         {'userId': '5e4c214a69cc03000caf6259', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 29, 'attempts': 0, 'success': True, 'time_success': 169.036, 'time_first': 24.919, 'timedout': False, 'examples': False},
#                         {'userId': '5e4c214a69cc03000caf6259', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 33, 'attempts': 0, 'success': True, 'time_success': 138, 'time_first': 32.678, 'timedout': False, 'examples': False},
#                         {'userId': '5e4c214a69cc03000caf6259', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 700, 'attempts': 14, 'success': True, 'time_success': 1736.211, 'time_first': 40.293, 'timedout': False, 'examples': False},
#                         {'userId': '5ede90720fb072121d859d1c', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 0, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
#                         {'userId': '5ede90720fb072121d859d1c', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 0, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
#                         {'userId': '5ede90720fb072121d859d1c', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 0, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
#                         {'userId': '5ede90720fb072121d859d1c', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 0, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
#                         {'userId': '5ede90720fb072121d859d1c', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 0, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
#                         {'userId': '5eda126ec6a418029cb19e91', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 6, 'attempts': 0, 'success': True, 'time_success': 30.988, 'time_first': 16.164, 'timedout': False, 'examples': False},
#                         {'userId': '5eda126ec6a418029cb19e91', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 33, 'attempts': 0, 'success': True, 'time_success': 125.935, 'time_first': 15.795, 'timedout': False, 'examples': True},
#                         {'userId': '5eda126ec6a418029cb19e91', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 72, 'attempts': 2, 'success': True, 'time_success': 216.632, 'time_first': 15.931, 'timedout': False, 'examples': True},
#                         {'userId': '5eda126ec6a418029cb19e91', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 0, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': True, 'examples': False},
#                         {'userId': '5eda126ec6a418029cb19e91', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 228, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': True},
#                         {'userId': '5f043ab655b1f267b94176b4', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 17, 'attempts': 1, 'success': True, 'time_success': 37.647, 'time_first': 8.845, 'timedout': False, 'examples': False},
#                         {'userId': '5f043ab655b1f267b94176b4', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 6, 'attempts': 0, 'success': True, 'time_success': 37.777, 'time_first': 31.252, 'timedout': False, 'examples': False},
#                         {'userId': '5f043ab655b1f267b94176b4', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 32, 'attempts': 0, 'success': True, 'time_success': 193.365, 'time_first': 53.24, 'timedout': False, 'examples': False},
#                         {'userId': '5f043ab655b1f267b94176b4', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 36, 'attempts': 4, 'success': True, 'time_success': 274.002, 'time_first': 26.042, 'timedout': False, 'examples': False},
#                         {'userId': '5f043ab655b1f267b94176b4', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 179, 'attempts': 8, 'success': True, 'time_success': 877.187, 'time_first': 19.982, 'timedout': False, 'examples': False},
#                         {'userId': '5f4bdd0445dcf109c307b90d', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 6, 'attempts': 1, 'success': True, 'time_success': 36.998, 'time_first': 18.498, 'timedout': False, 'examples': False},
#                         {'userId': '5f4bdd0445dcf109c307b90d', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 7, 'attempts': 0, 'success': True, 'time_success': 60.394, 'time_first': 22.531, 'timedout': False, 'examples': False},
#                         {'userId': '5f4bdd0445dcf109c307b90d', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 73, 'attempts': 2, 'success': True, 'time_success': 241.089, 'time_first': 31.961, 'timedout': False, 'examples': False},
#                         {'userId': '5f4bdd0445dcf109c307b90d', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 48, 'attempts': 2, 'success': True, 'time_success': 256.524, 'time_first': 24.316, 'timedout': False, 'examples': False},
#                         {'userId': '5f4bdd0445dcf109c307b90d', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 169, 'attempts': 6, 'success': True, 'time_success': 874.451, 'time_first': 23.271, 'timedout': False, 'examples': False},
#                         {'userId': '5eedb69308f7161ee954279d', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 17, 'attempts': 0, 'success': True, 'time_success': 77.774, 'time_first': 38.417, 'timedout': False, 'examples': False},
#                         {'userId': '5eedb69308f7161ee954279d', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 37, 'attempts': 0, 'success': True, 'time_success': 291.654, 'time_first': 61.648, 'timedout': False, 'examples': True},
#                         {'userId': '5eedb69308f7161ee954279d', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 67, 'attempts': 6, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': True, 'examples': True},
#                         {'userId': '5eedb69308f7161ee954279d', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 33, 'attempts': 0, 'success': True, 'time_success': 202.189, 'time_first': 32.765, 'timedout': False, 'examples': False},
#                         {'userId': '5eedb69308f7161ee954279d', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 81, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
#                         {'userId': '5dd5105a82569a4c04723f7e', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 15, 'attempts': 0, 'success': True, 'time_success': 29.218, 'time_first': 9.822, 'timedout': False, 'examples': False},
#                         {'userId': '5dd5105a82569a4c04723f7e', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 9, 'attempts': 0, 'success': True, 'time_success': 52.761, 'time_first': 28.749, 'timedout': False, 'examples': True},
#                         {'userId': '5dd5105a82569a4c04723f7e', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 129, 'attempts': 3, 'success': True, 'time_success': 236.083, 'time_first': 17.507, 'timedout': False, 'examples': False},
#                         {'userId': '5dd5105a82569a4c04723f7e', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 11, 'attempts': 1, 'success': True, 'time_success': 87.678, 'time_first': 12.674, 'timedout': False, 'examples': False},
#                         {'userId': '5dd5105a82569a4c04723f7e', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 369, 'attempts': 3, 'success': True, 'time_success': 692.283, 'time_first': 18.375, 'timedout': False, 'examples': False},
#                         {'userId': '5efb2cae4187a504713a4081', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 8, 'attempts': 2, 'success': True, 'time_success': 63.926, 'time_first': 18.388, 'timedout': False, 'examples': False},
#                         {'userId': '5efb2cae4187a504713a4081', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 8, 'attempts': 0, 'success': True, 'time_success': 34.096, 'time_first': 26.482, 'timedout': False, 'examples': False},
#                         {'userId': '5efb2cae4187a504713a4081', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 13, 'attempts': 0, 'success': True, 'time_success': 122.564, 'time_first': 38.631, 'timedout': False, 'examples': False},
#                         {'userId': '5efb2cae4187a504713a4081', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 11, 'attempts': 4, 'success': True, 'time_success': 187.785, 'time_first': 29.175, 'timedout': False, 'examples': False},
#                         {'userId': '5efb2cae4187a504713a4081', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 112, 'attempts': 0, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': True},
#                         {'userId': '5ed1717c9654ab0b17be2ceb', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 26, 'attempts': 2, 'success': True, 'time_success': 76.257, 'time_first': 14.77, 'timedout': False, 'examples': False},
#                         {'userId': '5ed1717c9654ab0b17be2ceb', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 17, 'attempts': 0, 'success': True, 'time_success': 82.59, 'time_first': 28.854, 'timedout': False, 'examples': True},
#                         {'userId': '5ed1717c9654ab0b17be2ceb', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 42, 'attempts': 0, 'success': True, 'time_success': 193.123, 'time_first': 23.634, 'timedout': False, 'examples': False},
#                         {'userId': '5ed1717c9654ab0b17be2ceb', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 17, 'attempts': 0, 'success': True, 'time_success': 107.22, 'time_first': 20.909, 'timedout': False, 'examples': False},
#                         {'userId': '5ed1717c9654ab0b17be2ceb', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 392, 'attempts': 9, 'success': True, 'time_success': 1201.432, 'time_first': 23.433, 'timedout': False, 'examples': False},
#                         {'userId': '5daec370e4688e00142ca236', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 10, 'attempts': 0, 'success': True, 'time_success': 51.123, 'time_first': 17.123, 'timedout': False, 'examples': True},
#                         {'userId': '5daec370e4688e00142ca236', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 45, 'attempts': 0, 'success': True, 'time_success': 227.917, 'time_first': 37.759, 'timedout': False, 'examples': False},
#                         {'userId': '5daec370e4688e00142ca236', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 77, 'attempts': 9, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': True, 'examples': False},
#                         {'userId': '5daec370e4688e00142ca236', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 29, 'attempts': 7, 'success': True, 'time_success': 311.635, 'time_first': 34.626, 'timedout': False, 'examples': False},
#                         {'userId': '5daec370e4688e00142ca236', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 191, 'attempts': 10, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': False},
#                         {'userId': '5fc8d1b43e9eb32a22d4da4d', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 18, 'attempts': 0, 'success': True, 'time_success': 78, 'time_first': 11.961, 'timedout': False, 'examples': True},
#                         {'userId': '5fc8d1b43e9eb32a22d4da4d', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 23, 'attempts': 0, 'success': True, 'time_success': 117.346, 'time_first': 10.148, 'timedout': False, 'examples': True},
#                         {'userId': '5fc8d1b43e9eb32a22d4da4d', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 188, 'attempts': 4, 'success': True, 'time_success': 440.708, 'time_first': 19.778, 'timedout': False, 'examples': True},
#                         {'userId': '5fc8d1b43e9eb32a22d4da4d', 'sessionId': 'Prolific Jan2021', 'item': 'Combine', 'actions': 110, 'attempts': 4, 'success': True, 'time_success': 205.766, 'time_first': 16.544, 'timedout': False, 'examples': False},
#                         {'userId': '5fc8d1b43e9eb32a22d4da4d', 'sessionId': 'Prolific Jan2021', 'item': 'Challenge', 'actions': 368, 'attempts': 12, 'success': True, 'time_success': 899.591, 'time_first': 41.294, 'timedout': False, 'examples': False},
#                         {'userId': '5c28efb626e55d0001a685b1', 'sessionId': 'Prolific Jan2021', 'item': 'Basic Commands', 'actions': 6, 'attempts': 0, 'success': True, 'time_success': 38.148, 'time_first': 16.823, 'timedout': False, 'examples': False},
#                         {'userId': '5c28efb626e55d0001a685b1', 'sessionId': 'Prolific Jan2021', 'item': 'Function', 'actions': 63, 'attempts': 0, 'success': True, 'time_success': 185.429, 'time_first': 32.272, 'timedout': False, 'examples': True},
#                         {'userId': '5c28efb626e55d0001a685b1', 'sessionId': 'Prolific Jan2021', 'item': 'Repeat', 'actions': 111, 'attempts': 3, 'success': False, 'time_success': 0, 'time_first': 0, 'timedout': False, 'examples': True}]
# )
#     df4['success'] = df4.success.astype('str')

#
# def create_dashboard(server):
#     """Create a Plotly Dash dashboard."""
#     dash_app = dash.Dash(
#         server=server,
#         routes_pathname_prefix='/dashapp/',
#         external_stylesheets=[
#             '/static/dist/css/styles.css',
#             'https://fonts.googleapis.com/css?family=Lato',
#             'https://codepen.io/chriddyp/pen/bWLwgP.css'
#         ]
#     )
#
#     ms_interval = 3 * 1000
#
#     tab_names = ['User View', 'Class View']
#     tables = []
#     for table in table_dict:
#         options = []
#         [options.append({'label': v, 'value': v}) for v in table_dict[table]['dropdown_list']]
#         tables.append(
#             Table(app=dash_app, data={'name': table_dict[table]['name'],
#                                             'tab':table_dict[table]['tab'],
#                                             'dropdown_col': table_dict[table]['dropdown_col'],
#                                             'options':options
#                                       }
#                   )
#                       )
#     options = []
#     [options.append({'label': k, 'value': k}) for k in dropdown_dict]
#    # store = dbb.Store(dash_app)
#     #store.register('intermediate-data')
#
#     # Custom HTML layout
#     dash_app.index_string = html_layout
#
#     dash_app.layout = \
#         html.Div([
#             dcc.Tabs(
#                     [dcc.Tab(
#                         label='tab',
#                         children =
#                         html.Div(
#                             [
#                                 dcc.Dropdown(id='dropdown-group', options=options,
#                                              placeholder='Select...'),
#                                 dcc.Dropdown(id='dropdown-user', placeholder='Select...'),
#                                 dash_table.DataTable(
#                                     id='data-table1',
#                                     page_action="native",
#                                     page_size=10,
#                                     style_data={'width': '100px'},
#                                     style_cell_conditional=[{'if': {'column_id': 'userId'},'width': '250px'}],
#                                     style_table={'overflowX': 'auto'},
#                                     columns = [{"name": i.capitalize(), "id": i} for i in ['sessionId', 'userId', 'item', 'n_actions', 'n_attempts', 'success','success_emoji',
#                                                                               'first_time', 'success_time', 'opened_example', 'timedout']],
#                                     style_data_conditional= [
#                                         {'if': {'column_id': 'success','filter_query': '{success} eq "True"'},'backgroundColor': 'rgba(60,179,113,.5)','color': 'transparent'},
#                                         {'if': {'column_id': 'success','filter_query': '{success} eq "False"'},'backgroundColor': 'rgba(240, 128, 128, .5)','color': 'transparent'},
#                                         {'if': {'column_id': 'opened_example', 'filter_query': '{opened_example} eq "True"'},
#                                          'backgroundColor': 'LightGreen', 'color': 'transparent'},
#                                         {'if': {'column_id': 'opened_example', 'filter_query': '{opened_example} eq "False"'},
#                                          'backgroundColor': 'LightCoral', 'color': 'transparent'},
#                                         {'if': {'column_id': 'timedout', 'filter_query': '{timedout} eq "True"'},
#                                          'backgroundColor': 'LightGreen', 'color': 'transparent'},
#                                         {'if': {'column_id': 'timedout', 'filter_query': '{timedout} eq "False"'},
#                                          'backgroundColor': 'LightCoral', 'color': 'transparent'}
#                                     ]
#                                 )
#                             ]
#                     #         [table.layout for table in tables if table.data.tab == tab]
#                     #     )
#                     # ) for tab in tab_names
#                         ))]
#             ),
#
#             dcc.Interval(
#                 id='track-interval',
#                 interval=ms_interval,  # in milliseconds,
#                 n_intervals=0
#             ),
#
#             html.Div(id='data-container', style={'display': 'none'})
#             #,
#             #store.layout
#         ], id='dash-container', className='row')
#
#     raw_data_list, read_time_list = FirestoreListener(collection_name='karelDB')
#
#     init_callbacks(dash_app, raw_data_list, tables, dropdown_dict)#, store)
#
#     return dash_app.server
#
#
# def init_callbacks(dash_app, raw_data_list, tables, dropdown_dict):#, store):
#
#     @dash_app.callback(
#         Output('data-container','children'),
#         [Input('track-interval', 'n_intervals')]
#     )
#     def query_data(n_intervals):
#         print("n_intervals is {}".format(n_intervals))
#         if len(raw_data_list) == 0:
#             return dash.no_update
#         else:
#             df = pd.DataFrame.from_records(raw_data_list)
#
#             # formatting and sorting by date
#             df['date'] = pd.to_datetime(df.date, format='%Y-%m-%dT%H:%M:%S.%fZ')
#             df.sort_values(by='date', inplace=True)
#
#             # Prolific length 15764
#             df['sessionId'] = np.where(
#                 (df.date > '2021-01-08') & (df.userId.astype(str).str.contains('-') == False) & (
#                             df.userId.astype(str).str.len() > 20),
#                 'Prolific Jan2021', 'Other')
#
#             user_df, avg_df = ResultsDataMaker(df)
#
#             print("Data ready with shapes {},{}....".format(user_df.shape, avg_df.shape))
#             return json.dumps({'user':user_df.to_json(),'avg':avg_df.to_json()})
#
#     @dash_app.callback(
#         Output('dropdown-user','options'),
#         [Input('dropdown-group', 'value')]
#     )
#     def dropdown_data(value):
#         options = []
#         [options.append({'label': v, 'value': v}) for v in dropdown_dict[value]]
#
#         return options
#
#
#     # for table in tables:
#     #     table.callbacks(
#     #         store.input('intermediate-data'),
#     #         Input('track-interval', 'n_intervals')
#     #     )
#
#     # @dash_app.callback(
#     #     Output('data-table1', 'data'),
#     #     [Input('data-container', 'children')]
#     # )
#     # def update_table(data_list):
#     #
#     #     if data_list is None:
#     #         print('{} is None'.format(data_list))
#     #         return dash.no_update
#     #     else:
#     #         print("data", data_list)
#     #         return data_list
#
#     @dash_app.callback(
#         Output('data-table1', 'data'),
#         [Input('dropdown-user', 'value'),Input('data-container','children')]
#     )
#     def update_output(value, dfs):
#         try:
#             ds = json.loads(dfs) #⭐
#             df = pd.read_json(ds['user'], orient='records').astype('str') #actually needed only for boolean
#             df['success_emoji'] = df['success'].apply(lambda x: '✅' if x == 'True' else '⭕')
#             return df.loc[df.userId == value].to_dict('records')
#
#         except TypeError as e:
#             print(e)
#             return dash.no_update


# table_dict = {
#     'table1' : {'name':'User performance',
#                 'dropdown_col':'userId',
#                 'dropdown_list':['59dbee057f3d71000171d37d', '5d694784be10f9001511d7a3',
#        '5f512f610a752a32cf96d74f', '5ca8c84e92fdc200129e9db3',
#        '5e4c214a69cc03000caf6259', '5ede90720fb072121d859d1c',
#        '5eda126ec6a418029cb19e91', '5f043ab655b1f267b94176b4',
#        '5f4bdd0445dcf109c307b90d', '5eedb69308f7161ee954279d',
#        '5dd5105a82569a4c04723f7e', '5efb2cae4187a504713a4081',
#        '5ed1717c9654ab0b17be2ceb', '5daec370e4688e00142ca236',
#        '5fc8d1b43e9eb32a22d4da4d', '5c28efb626e55d0001a685b1',
#        '5fc3df4c86fa277559d373c2', '5b80b3ba16aa4400016a75ef',
#        '5dde8068332b34dd9047e51b', '5c44ad201ddd660001ca00b0',
#        '5fc0c541c266bd597b286e98', '5f248b7b1bde03086270bd37',
#        '5e444fa46bcdba04dcf2d695', '5ec970f3e657d60c8e4db3a4',
#        '5cfd119645e1a20001883ee6', '5b914a5f02a76000015c72d4',
#        '5fa2be9d820efd4e33eee9fc', '5fdde74bfdb6e64c26da591a',
#        '5c102d91e32f860001651a93', '5f9bdffe42555942fbc9ca49',
#        '5c7fb04093cdce00160adf49', '5de631043cf27959fe70269c',
#        '5f2ab8c4c46fc63609d8eedb', '5bc2e0ec4f3bfd00012e97b5',
#        '5eb8630fb9a7c17ac8c7d14b'],
#                 'tab': 'User View'
#                 },
#     'table2': {'name': 'Group performance',
#                'dropdown_col': 'sessionId',
#                'dropdown_list': ['Prolific Jan2021'],
#                'tab': 'User View'
#                },
#     'table3': {'name': 'Class performance',
#                'dropdown_col': 'metricId',
#                'dropdown_list': ['actions', 'attempts', 'success', 'time_success','time_first','timedout','examples'],
#                'tab': 'Class View'
#                },
#     }


#old tools.py
# """Instantiate a Dash app."""
# import numpy as np
# import pandas as pd
# import dash
# import dash_table
# import dash_html_components as html
# import dash_core_components as dcc
# from dash.dependencies import Input, Output
#
# from .data import CreateDataFrame #changed from create_dataframe
# from .layout import html_layout
# import plotly.express as px
# import datetime, time
# from .filemanager import FirestoreListener, CreateTable, IndexFlattener, DataBars, MaxValueTableStyler
# from google.cloud import firestore
# from collections import Counter
#
#
#
# def create_dashboard(server):
#     """Create a Plotly Dash dashboard."""
#     dash_app = dash.Dash(
#         server=server,
#         routes_pathname_prefix='/dashapp/',
#         external_stylesheets=[
#             '/static/dist/css/styles.css',
#             'https://fonts.googleapis.com/css?family=Lato',
#             'https://codepen.io/chriddyp/pen/bWLwgP.css'
#         ]
#     )
#
#     ms_interval = 60 * 1000
#
#     # Custom HTML layout
#     dash_app.index_string = html_layout
#
#     table_columns = ['userId','outcome','ModifyMoves', 'CommandsMLMR','KarelDrifts', 'KarelMoves']
#     opts = [{'label': i, 'value': i} for i in table_columns]
#
#     table_metrics = ['attempts','successes']
#     metrics = [{'label': i.capitalize(), 'value':i} for i in table_metrics]
#
#     dash_app.layout = \
#         html.Div([
#         dcc.Tabs([
#                      dcc.Tab(label="Tab one", children=[
#                                                                  html.Div([
#                                                                      html.Label("Select currentView of interest"),
#                                                                      dcc.Dropdown(id='opt',
#                                                                                   options=opts,
#                                                                                   value=table_columns,
#                                                                      multi = True)], style = {'fontSize':'20px','color':'#808080','display': 'inline-block','padding-top': '20px'}, className='four columns'),
#                          html.Div([
#                              dash_table.DataTable(
#                                  id='data-table',
#                                  row_selectable='multi',
#                                  selected_rows= [],
#                                  column_selectable = 'multi',
#                                  selected_columns=[],
#                                  sort_action="native",
#                                  sort_mode='native',
#                                  page_size=300,
#                                  style_cell={'textAlign': 'left'},
#                                  style_header={
#                                      'backgroundColor': 'rgb(230, 230, 230)',
#                                      'fontWeight': 'bold'
#                                  }
#                              )
#                          ],style={'padding-top': '20px'}, className='eight columns')
#                         ]),
#                 dcc.Tab(label="Tab two",children=[   html.Div([
#                              dash_table.DataTable(
#                                  id='data-table2',
#                                  sort_action="native",
#                                  sort_mode='native',
#                                  page_action = 'native',
#                                  page_size=10,
#                                 style_cell = {'textAlign': 'left'},
#                                  style_header={
#                                      'border': '1px solid rgb(189,189,210)',
#                                      'backgroundColor': 'rgb(230, 230, 230)',
#                                      'fontWeight': 'bold'})
#                          ], style={'padding-top': '20px'}, className='four columns'),
#                 html.Div([dcc.Graph(
#                     id='bar-graph')],style={'padding-top': '20px'}, className='eight columns')]),
#                 dcc.Tab(label="Tab three", children = html.Div([html.Div(html.H1("Select metric of interest"),style={'padding-top': '20px'}),
#                                                                      html.Div(dcc.Dropdown(
#                                                                          id='opt-3',
#                                                                                   options= metrics,
#                                                                                   value=table_metrics[0],
#                                                                                   multi = False),
#                                                                      style={'padding-bottom': '20px', 'padding-top': '10px'}),
#                                                                 html.Div(dash_table.DataTable(
#                     id='data-table3',
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     row_selectable="multi",
#                     selected_rows=[],
#                     page_action="native",
#                     page_size=10)),
#                     html.Div(id = 'graph-container')
#                                                                 ])
#                         )
#         ]),
#             dcc.Interval(
#                 id='track-interval',
#                 interval=ms_interval,  # in milliseconds,
#                 n_intervals=0)
#         ], id='dash-container', className='row')
#
#     results, read_time_list = FirestoreListener(collection_name='karelDB')
#
#     init_callbacks(dash_app, results, read_time_list, ms_interval)
#
#     return dash_app.server
#
#
#
# def init_callbacks(dash_app, results, read_time_list, ms_interval):
#
#
#     #tab3
#     @dash_app.callback(
#         [
#             Output('graph-container','children'),
#          Output('data-table3','columns'),
#          Output('data-table3','data'),
#          ],
#         [Input('track-interval', 'n_intervals'),
#          Input('data-table3', 'selected_rows'),
#          Input('opt-3', 'value')
#          ]
#     )
#     def update_graphseries(rows,
#                            user_selected_rows,
#                            value
#                            ):
#
#         if user_selected_rows is None:
#             user_selected_rows = []
#
#         df_tab3 = pd.DataFrame(CreateTable(['userId', 'data', 'type', 'currentView'], results))
#
#         dic_tab3 = {}
#
#         col = value
#
#         if col == 'attempts':
#             cond = (df_tab3.type.str.startswith("RUN_DONE"))
#         else:
#             cond = (df_tab3.type.str.startswith("RUN_DONE"))&(df_tab3.data.str.startswith('successful'))
#
#         dic_tab3[col] = pd.DataFrame(df_tab3[
#             cond].groupby(
#             ['userId', 'currentView']).count()['data'])
#
#         dic_tab3[col] = pd.pivot_table(dic_tab3[col], index=['userId'], columns='currentView').fillna(
#     0).reset_index()
#
#         dic_tab3[col][dic_tab3[col].columns[1:]] = dic_tab3[col][dic_tab3[col].columns[1:]].astype('int')
#
#         dic_tab3[col] = IndexFlattener(dic_tab3[col])
#
#
#         colors = ['#7FDBFF' if i in user_selected_rows else '#0074D9'
#                    for i in range(len(dic_tab3[col]))]
#
#         data = dic_tab3[col].to_dict('records')
#         columns = [{"name": i, "id": i, "selectable": True} for i in dic_tab3[col].columns]
#
#         #make columns selectable
#         #number of actions before completions, times it saw example?
#
#         graph = [html.Div(dcc.Graph(
#                 id=column,
#                 figure={
#                     "data": [
#                         {
#                             "x": dic_tab3[col]["userId"],
#                             "y": dic_tab3[col][column],
#                             "type": "bar",
#                             "marker": {"color": colors},
#                         }
#                     ],
#                     "layout": {
#                         "xaxis": {"automargin": True,
#                                   'tickangle': -90},
#                         "yaxis": {
#                             "automargin": True
#                         },
#                         "height": 350,
#                         #'paper_bgcolor' : 'rgba(103,128,159,0.5)',
#                         'plot_bgcolor' : 'rgba(171, 183, 183, 0.2)',
#                         "margin": {"t":30, "l": 10, "r": 10},
#                         "title": {
#         'text': column,
#         'y': 0.97,
#         'x':0.5,
#         'xanchor': 'center',
#         'yanchor': 'top'}
#                     },
#                 },
#             ),
#             className= 'three columns'
#         )
#             for column in dic_tab3[col].columns[1:]]
#
#         return graph, columns, data
#
#
#
#
#     #tab1
#     @dash_app.callback(
#         [Output('data-table','data'), Output('data-table','columns'), Output('data-table','style_data_conditional')],
#         [Input('track-interval', 'n_intervals'),Input('opt', 'value'),Input('data-table', 'selected_rows'), Input('data-table', 'selected_columns')]
#     )
#     def update_tables(rows, values, user_selected_rows, user_selected_columns):
#
#         #df = CreateTable('data', results)
#         if (read_time_list[-1].timestamp() * 1000 < datetime.datetime.utcnow().timestamp() * 1000 - ms_interval):
#
#             print('nothing has changed between {} and now {}'.format(read_time_list[-1], datetime.datetime.utcnow()))
#             try:
#                 df_tab1
#             except NameError:
#                 print('df doesn\'t exist')
#                 df_tab1 = pd.DataFrame(CreateTable(['userId', 'data', 'type', 'currentView'], results))
#
#                 df_tab1 = pd.DataFrame(
#                     df_tab1[(df_tab1.type.str.startswith("RUN_DONE"))].groupby(['userId', 'currentView'])['data'].value_counts() /
#                     df_tab1[
#                         (df_tab1.type.str.startswith("RUN_DONE"))].groupby(['userId', 'currentView'])[
#                         'data'].count() * 100).rename(columns={'data': 'frequency'}).reset_index()
#
#                 df_tab1 = pd.pivot_table(df_tab1, index=['userId', 'data'], columns='currentView').fillna(0).reset_index().rename(
#                     columns={'data': 'outcome'})
#
#                 df_tab1 = IndexFlattener(df_tab1)
#             else:
#                 print('df exists')
#                 pass
#         else:
#             print('something has changed between {} and now {}'.format(read_time_list[-1], datetime.datetime.utcnow()))
#
#             df_tab1 = pd.DataFrame(CreateTable(['userId', 'data', 'type', 'currentView'], results))
#
#             df_tab1 = pd.DataFrame(
#                 df_tab1[(df_tab1.type.str.startswith("RUN_DONE"))].groupby(['userId', 'currentView'])['data'].value_counts() / df_tab1[
#                     (df_tab1.type.str.startswith("RUN_DONE"))].groupby(['userId', 'currentView'])[
#                     'data'].count() * 100).rename(columns={'data': 'frequency'}).reset_index()
#
#             df_tab1 = pd.pivot_table(df_tab1, index=['userId', 'data'], columns='currentView').fillna(0).reset_index().rename(
#                 columns={'data': 'outcome'})
#
#             df_tab1 = IndexFlattener(df_tab1)
#
#
#
#         #filter rows based on selected_rows
#         if user_selected_rows is None:
#             print('row list is empty')
#             user_selected_rows = []
#         elif len(user_selected_rows) != 0:
#             [print(row) for row in user_selected_rows]
#             df_tab1 = df_tab1.iloc[user_selected_rows]
#         else:
#             pass
#
#
#
#         # filter out currentview based on dropdown
#         df_tab1 = df_tab1[values].round(1)
#
#         # filter columns based on selected_columns
#         if user_selected_columns is None:
#             print('col list is empty')
#             user_selected_columns = []
#         elif len(user_selected_columns) != 0:
#             [print(col) for col in user_selected_columns]
#             # df_tab1 = df_tab1[user_selected_columns]
#         else:
#             pass
#
#         data = df_tab1.to_dict('records')
#
#         columns = [{"name": i, "id": i, "selectable": True} for i in df_tab1.columns]
#
#
#
#         style_data_conditional = MaxValueTableStyler(df_tab1)
#         style_data_list = []
#         for val in values:
#
#             if (val == "userId") or (val == "outcome"):
#                 pass
#             else:
#                 #print("{} added to style list".format(val))
#                 style_data_list.extend(DataBars(df_tab1,val))
#
#         style_data_conditional =style_data_list
#
#         return data, columns, style_data_conditional
#
#     #tab2
#     @dash_app.callback(
#         [Output('bar-graph', 'figure'), Output('data-table2','data'), Output('data-table2','columns') ],
#         [Input('track-interval', 'n_intervals')]
#     )
#     def update_graphs(rows):
#         #if latest readtime different from current, update. how about first caase?
#         #if latest_read_time
#         if (read_time_list[-1].timestamp() * 1000 < datetime.datetime.utcnow().timestamp() * 1000 - ms_interval):
#
#             print('nothing has changed between {} and now {}'.format(read_time_list[-1], datetime.datetime.utcnow()))
#             try:
#                 df_tab2
#             except NameError:
#                 print('df doesn\'t exist')
#                 counter = Counter(CreateTable(['data'], results)['data'])
#                 df_tab2 = pd.DataFrame(list(counter.items()), columns=['Action', 'Count']).sort_values('Count',ascending=False)
#                 df_tab2 = df_tab2[~(df_tab2.Action.str.contains("xml"))]
#
#             else:
#                 print('df exists')
#                 pass
#         else:
#             print('something has changed between {} and now {}'.format(read_time_list[-1],datetime.datetime.utcnow()))
#             counter = Counter(CreateTable(['data'], results)['data'])
#             df_tab2 = pd.DataFrame(list(counter.items()), columns=['Action', 'Count']).sort_values('Count',ascending=False)
#             df_tab2 = df_tab2[~(df_tab2.Action.str.contains("xml"))]
#
#
#         fig = px.bar(df_tab2, x='Action', y='Count', opacity = 0.6)
#
#         # Customize aspect
#         fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
#                           marker_line_width=1.5, opacity=0.6)
#
#         fig.update_layout(title_text='Count of user action as of {}'.format(datetime.datetime.utcnow().strftime("%Y-%m-%d, %H:%M:%S")))
#
#
#         data = df_tab2.to_dict('records')
#
#         columns = [{"name": i, "id": i} for i in df_tab2.columns]
#
#         return fig, data, columns
#
#
#
#
#
# #last working version
# def create_dashboard(server):
#     """Create a Plotly Dash dashboard."""
#     dash_app = dash.Dash(
#         server=server,
#         routes_pathname_prefix='/dashapp/',
#         external_stylesheets=[
#             '/static/dist/css/styles.css',
#             'https://fonts.googleapis.com/css?family=Lato',
#             'https://codepen.io/chriddyp/pen/bWLwgP.css'
#         ]
#     )
#
#     ms_interval = 6 * 1000
#
#     # Custom HTML layout
#     dash_app.index_string = html_layout
#
#     table_columns = ['userId','outcome','ModifyMoves', 'CommandsMLMR','KarelDrifts', 'KarelMoves']
#     opts = [{'label': i, 'value': i} for i in table_columns]
#
#     table_metrics = ['attempts']
#     metrics = [{'label': i.capitalize(), 'value':i} for i in table_metrics]
#
#     dash_app.layout = \
#         html.Div([
#             dcc.Tabs([
#                 dcc.Tab(label="Tab three",
#                         children = html.Div(
#                             [
#                                 html.Div(
#                                     dash_table.DataTable(
#                                         id='data-table3',
#                                         filter_action="native",
#                                         sort_action="native",
#                                         sort_mode="multi",
#                                         page_action="native",
#                                         page_size=10
#                                     )
#                                 ),
#                         # this below is the div for the plots
#                         html.Div(id = 'graph-container')
#                             ]
#                         )
#                         )
#             ]),
#             dcc.Interval(
#                 id='track-interval',
#                 interval=ms_interval,  # in milliseconds,
#                 n_intervals=0
#             ),
#             html.Div(id='intermediate-value', style={'display': 'none'})
#         ], id='dash-container', className='row')
#
#     results, read_time_list = FirestoreListener(collection_name='karelDB')
#
#     init_callbacks(dash_app, results, read_time_list, ms_interval, table_metrics)
#
#     return dash_app.server
#
#
# def init_callbacks(dash_app, results, read_time_list, ms_interval, table_metrics):
#
#     @dash_app.callback(
#         Output('intermediate-value', 'children'),
#         [Input('track-interval', 'n_intervals')]
#     )
#     def query_data(n_intervals):
#
#         df_raw = pd.DataFrame(CreateTable(['userId', 'data', 'type', 'currentView'], results))
#
#         if len(df_raw) == 0:
#             return dash.no_update
#         else:
#             dic_tab3 = {}
#
#             cond = (df_raw.type.str.startswith("RUN_DONE")) # & (df_tab3.data.str.startswith('successful'))
#
#             df_grouped = pd.DataFrame(
#                 df_raw[cond].groupby(
#                     ['userId', 'currentView']).count()['data']
#             )
#
#             col = table_metrics[0]
#
#             dic_tab3[col] = pd.pivot_table(df_grouped, index=['userId'], columns='currentView').fillna(
#                 0).reset_index()
#
#             #formatting int
#             dic_tab3[col][dic_tab3[col].columns[1:]] = dic_tab3[col][dic_tab3[col].columns[1:]].astype('int')
#
#             dic_tab3[col] = IndexFlattener(dic_tab3[col])
#
#             #this could become a dict of dict eg. level 1 key tab, level 2 key table in tab
#             dic_tab3[col] =  dic_tab3[col].to_json(orient='split', date_format='iso')
#             return json.dumps(dic_tab3)
#
#     @dash_app.callback(
#         [
#             Output('data-table3', 'data'),
#             Output('data-table3', 'columns')
#          ],
#         [Input('intermediate-value', 'children')]
#     )
#     def update_table(dfs):
#
#         if dfs is None:
#             return dash.no_update
#         else:
#             datasets = json.loads(dfs)
#
#             value = table_metrics[0]
#
#             dic_tab3 = pd.read_json(datasets[value], orient='split')
#
#             colors = ['#0074D9' for i in range(len(dic_tab3))]
#
#             data = dic_tab3.to_dict('records')
#             columns = [{"name": i, "id": i, "selectable": True} for i in dic_tab3.columns]
#
#             #make columns selectable
#             #number of actions before completions, times it saw example?
#
#             graph = [html.Div(dcc.Graph(
#                     id=column,
#                     figure={
#                         "data": [
#                             {
#                                 "x": dic_tab3["userId"],
#                                 "y": dic_tab3[column],
#                                 "type": "bar",
#                                 "marker": {"color": colors},
#                             }
#                         ],
#                         "layout": {
#                             "xaxis": {"automargin": True,
#                                       'tickangle': -90},
#                             "yaxis": {
#                                 "automargin": True
#                             },
#                             "height": 350,
#                             #'paper_bgcolor' : 'rgba(103,128,159,0.5)',
#                             'plot_bgcolor' : 'rgba(171, 183, 183, 0.2)',
#                             "margin": {"t":30, "l": 10, "r": 10},
#                             "title": {
#             'text': column,
#             'y': 0.97,
#             'x':0.5,
#             'xanchor': 'center',
#             'yanchor': 'top'}
#                         },
#                     },
#                 ),
#                 className= 'three columns'
#             )
#                 for column in dic_tab3.columns[1:]]
#
#             return data, columns
#
