from google.cloud import firestore
import pandas as pd
import threading


def IntermediateDataMaker(df, columns):
    '''add descr'''

    dic_tab = {}

    # cond and groupby could become inputs
    cond = (df.type.str.startswith("RUN_DONE"))  # & (df_tab3.data.str.startswith('successful'))

    df_grouped = pd.DataFrame(
        df[cond].groupby(
            ['userId', 'currentView']).count()['data']
    )

    for col in columns:
        dic_tab[col] = pd.pivot_table(df_grouped, index=['userId'], columns='currentView').fillna(
            0).reset_index()

        # formatting int
        dic_tab[col][dic_tab[col].columns[1:]] = dic_tab[col][dic_tab[col].columns[1:]].astype('int')

        dic_tab[col] = IndexFlattener(dic_tab[col])

        # this could become a dict of dict eg. level 1 key tab, level 2 key table in tab
        dic_tab[col] = dic_tab[col].to_json(orient='split', date_format='iso')

    return dic_tab


def FirestoreListener(collection_name: str = 'karelDB'):
    db = firestore.Client.from_service_account_json("keys/pila-277913-44ed571ccec0.json")

    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    firestore_collection = []

    read_time_list = []

    ## The  provided callback is run on the snapshot of the documents.
    def on_snapshot(collection_snapshot, changes, read_time):
        for doc in collection_snapshot:
            firestore_collection.append(doc.to_dict())

        read_time_list.append(read_time)

        callback_done.set()

    collection_query = db.collection(collection_name)  # .where(u'state', u'==', u'CA')

    # Watch the collection query
    query_watch = collection_query.on_snapshot(on_snapshot)

    return firestore_collection, read_time_list


def ReadFirestoreCollection(collection_name: str = "karelDB"):

    db = firestore.Client.from_service_account_json("keys/pila-277913-44ed571ccec0.json")

    firestore_collection = []
    [firestore_collection.append(dic.to_dict()) for dic in db.collection(collection_name).stream()]

    return firestore_collection



def ReadFirestoreDocument(doc_name: str, collection_name: str = "karelDB"):

    db = firestore.Client.from_service_account_json("keys/pila-277913-44ed571ccec0.json")

    doc_ref = db.collection(collection_name).document(doc_name)
    doc = doc_ref.get()

    return doc.to_dict()



def TimeConverter(timecol, fmt="%Y-%m-%dT%H:%M:%S.%fZ"):
    '''Converts time feature to a given format'''
    return pd.to_datetime(timecol, format=fmt)


def CreateTable(
        key_names: [],
        list_dict_name: str
):
    table = {}
    # add sorting by timestamp
    # [table.append(ev.get(key_name)) for key_name in key_names for ev in dict_name]
    for key_name in key_names:

        table[key_name] = []

        for ev in list_dict_name:
            table[key_name].append(ev.get(key_name))

    return table


def IndexFlattener(df):
    '''add desc'''
    for col in df.columns:
        if col[1] == '':
            pass
        else:
            df[col[1]] = df[col]
            df = df.drop(col, axis=1)

    df.columns = df.columns.get_level_values(0)

    return df

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
                    #9ECAE1 0%,
                    #9ECAE1 {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2,
            'paddingLeft': 2,
            'paddingRight': 2
        })

    return styles


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