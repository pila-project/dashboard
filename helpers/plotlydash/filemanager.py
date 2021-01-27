from google.cloud import firestore
import pandas as pd
import numpy as np
import threading
from collections import Counter
import datetime

def DataBars(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #6eb08c 0%,
                    #6eb08c {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles

def FirestoreListener(collection_name: str = 'karelDB'):
    db = firestore.Client.from_service_account_json("keys/pila-277913-44ed571ccec0.json")

    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    firestore_collection = []

    read_time_list = []

    ## The  provided callback is run on the snapshot of the documents.
    def on_snapshot(collection_snapshot, changes, read_time):
        # for doc in collection_snapshot:
        #     if doc.to_dict() not in firestore_collection:
        #         firestore_collection.append(doc.to_dict())
        #     else:
        #         pass
        [firestore_collection.append(doc.to_dict()) for doc in collection_snapshot if doc.to_dict() not in firestore_collection]
        read_time_list.append(read_time)

        callback_done.set()

    collection_query = db.collection(collection_name)  # .where(u'state', u'==', u'CA')

    # Watch the collection query
    query_watch = collection_query.on_snapshot(on_snapshot)

    return firestore_collection, read_time_list


def ReadFirestoreCollection(db_name: str = "karelDB"):

    db = firestore.Client.from_service_account_json("keys/pila-277913-44ed571ccec0.json")
    print('Reading data at {}'.format(datetime.datetime.now()))
    firestore_collection = []
    [firestore_collection.append(doc.to_dict()) for doc in db.collection(db_name).stream() if doc.to_dict() not in firestore_collection]
    print('Returning data at {}'.format(datetime.datetime.now()))
    return firestore_collection





def MaxValueTableStyler(df):
    if 'id' in df:
        numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
    else:
        numeric_columns = df.select_dtypes('number')
    max_across_numeric_columns = numeric_columns.max()
    max_across_table = max_across_numeric_columns.max()
    styles = []
    for col in max_across_numeric_columns.keys():
        if max_across_numeric_columns[col] == max_across_table:
            styles.append({
                'if': {
                    'filter_query': '{{{col}}} = {value}'.format(
                        col=col, value=max_across_table
                    ),
                    'column_id': col
                },
                'backgroundColor': '#39CCCC',
                'color': 'white'
            })
    return styles


def ResultsDataMaker(df):
    '''input; pandas.df
    output: pandas.df for user and avg'''

    #if item list changes, update example list correspondingly
    item_list = ['Basic Commands', 'Function', 'Repeat', 'Combine', 'Challenge']

    example_list = ['CommandsHouseGood', 'CommandsHouseBad',
                    'MethodsTurnAroundBad', "MethodsTurnAroundGood",
                    "RepeatL2StepUpGood", "RepeatL2StepUpBad",
                    'RepeatL3Dash5Good', 'RepeatL3Dash5Bad',
                    'DiamondGood', 'DiamondBad']
    #results df
    #print('Defining results dataframes....')
    user_df = df[['sessionId','userId','item']].loc[df.item.isin(item_list)].drop_duplicates(inplace=False).reset_index().drop('index', axis=1, inplace=False)
    avg_df = df[['sessionId','item']].loc[df.item.isin(item_list)].drop_duplicates(inplace=False).reset_index().drop('index', axis=1, inplace=False)

    #actions
    #print('Number of actions...')
    avg_actions_df = (df.loc[(df.type=="UPDATE_CODE_move")|(df.type=="UPDATE_CODE_delete") & (df.item.isin(item_list))].groupby(['sessionId','item'])['type'].count()/\
               df.loc[(df.type=="UPDATE_CODE_move")|(df.type=="UPDATE_CODE_delete")& (df.item.isin(item_list))].groupby(['sessionId','item']).nunique()['userId']).reset_index()
    avg_df = pd.merge(avg_df, avg_actions_df, how='left',on=['sessionId','item'])
    avg_df.rename(columns={0:'avg_n_actions'}, inplace=True)

    actions_df = df.loc[((df.type=="UPDATE_CODE_move")|(df.type=="UPDATE_CODE_delete")) & (df.item.isin(item_list))].groupby(['sessionId','userId','item'])['type'].count().reset_index()
    user_df = pd.merge(user_df, actions_df, how='left',on=['sessionId','userId','item'])
    user_df.rename(columns={'type':'n_actions'}, inplace=True)

    #attempts
    #print('Number of attempts...')

    avg_attempts_df = (df.loc[(df.type=="RUN_DONE") & (df.data=="unsuccessful") & (df.item.isin(item_list))].groupby(['sessionId','item'])['data'].count()/\
                df.loc[(df.type=="RUN_DONE") & (df.data=="unsuccessful") & (df.item.isin(item_list))].groupby(['sessionId','item']).nunique()['userId']).reset_index()
    avg_df = pd.merge(avg_df, avg_attempts_df, how='left',on=['sessionId','item'])
    avg_df.rename(columns={0:'avg_n_attempts'}, inplace=True)
    avg_df.fillna(0,inplace=True)

    attempts_df = df.loc[(df.type=="RUN_DONE") & (df.data=="unsuccessful") & (df.item.isin(item_list))].groupby(['sessionId','userId','item'])['data'].count().reset_index()
    user_df = pd.merge(user_df, attempts_df, how='left',on=['sessionId','userId','item'])
    user_df.rename(columns={'data':'n_attempts'}, inplace=True)
    user_df.fillna(0,inplace=True)

    #success % all users in the session
    #print('Number of successes...')
    avg_success_df = ((df.loc[(df.type=="RUN_DONE") & (df.data=="successful") & (df.item.isin(item_list))].groupby(['sessionId','item']).nunique()['userId']/\
                   df.loc[df.item.isin(item_list)].groupby(['sessionId','item']).nunique()['userId']*100).fillna(0)).reset_index()
    avg_df = pd.merge(avg_df, avg_success_df, how='left',on=['sessionId','item'])
    avg_df.rename(columns={'userId':'avg_n_successes'}, inplace=True)

    success_df = (df.loc[(df.type=="RUN_DONE") & (df.data=="successful") & (df.item.isin(item_list))].groupby(
        ['sessionId','userId','item'])['data'].count()).reset_index() #replace positive examples with True and add negative with False
    user_df = pd.merge(user_df, success_df, how='left',on=['sessionId','userId','item'])
    user_df.rename(columns={'data':'success'}, inplace=True)
    user_df['success'] =np.where(user_df['success']>0,True,False)

    #time metrics
    #print('Time metrics...')

    start_df = df.loc[(df.currentView == 'dashboard')& (df.item.isin(item_list))].groupby(['sessionId','userId','item'])['date'].apply(lambda x: x.tolist()[0]).reset_index()
    first_df=df.loc[(df.item.isin(item_list))].groupby(['sessionId','userId','item'])['date'].apply(lambda x: x.tolist()).reset_index()
    end_df=df.loc[(df.data == 'successful') & (df.type == 'RUN_DONE') & (df.item.isin(item_list))].groupby(['sessionId','userId','item'])['date'].apply(lambda x: x.tolist()[0]).reset_index()

    #preprocessing
    date_list = []
    for row in first_df.date.values:
        try:
            date_list.append(row[3])
        except IndexError as e:
            date_list.append(row[-1])

    first_df['first_date'] = date_list

    end_df.rename(columns={'date':'end_date'},inplace =True)
    start_df.rename(columns={'date':'start_date'},inplace =True)

    time_df = pd.merge(start_df,first_df,on=['sessionId','userId','item'], how='left')
    time_df = pd.merge(time_df,end_df,on=['sessionId','userId','item'], how='left')

    time_df['timeto_first_action'] = ((time_df['first_date']- time_df['start_date']).fillna(pd.Timedelta(seconds=0)))/\
                             np.timedelta64(1, 's')
    time_df['timeto_success'] = ((time_df['end_date']- time_df['start_date']).fillna(pd.Timedelta(seconds=0)))/\
                           np.timedelta64(1, 's')

    #time_first
    #print('Time to first action...')
    avg_first_df = time_df.groupby(['sessionId','item'])['timeto_first_action'].mean().apply(fs).reset_index()
    avg_df = pd.merge(avg_df, avg_first_df, how='left',on=['sessionId','item'])
    avg_df.rename(columns={'timeto_first_action':'avg_timeto_first_action'}, inplace=True)

    time_df['timeto_first_action'] = (((time_df['first_date']- time_df['start_date']).fillna(pd.Timedelta(seconds=0)))/\
                              np.timedelta64(1, 's')).apply(fs) #format to string after computing the session average

    #time_success
    #print('Time to success...')
    avg_end_df = time_df.groupby(['sessionId','item'])['timeto_success'].mean().apply(fs).reset_index()
    avg_df = pd.merge(avg_df, avg_end_df, how='left',on=['sessionId','item'])
    avg_df.rename(columns={'timeto_success':'avg_timeto_success'}, inplace=True)

    time_df['timeto_success'] = (((time_df['end_date']- time_df['start_date']).fillna(pd.Timedelta(seconds=0)))/ np.timedelta64(1, 's')).apply(fs)
    user_df = pd.merge(user_df, time_df, how='left',on=['sessionId','userId','item'])
    user_df.drop(['start_date', 'date', 'first_date',
           'end_date'], axis=1, inplace=True)

    #opened example
    #print('Opened examples...')
    avg_opedexample_df=((df.loc[(df.type == "UPDATE_CURRENT_VIEW") & (df.data.isin(example_list)) & (df.item.isin(item_list))].groupby(['sessionId','item']).nunique()['userId']/\
                   df.loc[df.item.isin(item_list)].groupby(['sessionId','item']).nunique()['userId']*100).fillna(0)).reset_index()
    avg_df = pd.merge(avg_df, avg_opedexample_df, how='left',on=['sessionId','item'])
    avg_df.rename(columns={'userId':'avg_opened_example'}, inplace=True)

    opedexample_df=df.loc[(df.type == "UPDATE_CURRENT_VIEW") & (df.data.isin(example_list)) & (df.item.isin(item_list))].groupby(['sessionId','userId','item'])['data'].count().reset_index()
    user_df = pd.merge(user_df, opedexample_df, how='left',on=['sessionId','userId','item'])
    user_df.rename(columns={'data':'opened_example'}, inplace=True)
    user_df['opened_example'] =np.where(user_df['opened_example']>0,True,False)

    #timedout
    #print('Timedout...')
    avg_timedout_df = ((df.loc[(df.type=="TIMEDOUT") & (df.item.isin(item_list))].groupby(['sessionId','item']).nunique()['userId']/\
                   df.loc[df.item.isin(item_list)].groupby(['sessionId','item']).nunique()['userId']*100).fillna(0)).reset_index()

    avg_df = pd.merge(avg_df, avg_timedout_df, how='left',on=['sessionId','item'])
    avg_df.rename(columns={'userId':'avg_timedout'}, inplace=True)

    timedout_df = df.loc[(df.type=="TIMEDOUT") & (df.item.isin(item_list))].groupby(['sessionId',"userId",'item'])['data'].count()
    user_df = pd.merge(user_df, timedout_df, how='left',on=['sessionId','userId','item'])
    user_df.rename(columns={'data':'timedout'}, inplace=True)
    user_df['timedout'] =np.where(user_df['timedout']>0,True,False)

    #print('Exporting results...')
    return user_df, avg_df

def fs(x):
    ts = x
    # ts = x.total_seconds()
    hours, remainder = divmod(ts, 3600)
    minutes, seconds = divmod(remainder, 60)
    return ('{:02d}:{:02d}').format(int(minutes), int(seconds))