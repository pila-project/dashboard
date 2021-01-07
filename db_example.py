from google.cloud import firestore
import threading
import pandas as pd

callback_done = threading.Event()
firestore_collection = []
read_time_list = []


def on_snapshot(collection_snapshot, changes, read_time):
    for doc in collection_snapshot:
        firestore_collection.append(doc.to_dict())
    read_time_list.append(read_time)
    callback_done.set()

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

db = firestore.Client.from_service_account_json("keys/pila-277913-44ed571ccec0.json") #replace with your gcp private key

collection_name = 'karelDB'
collection_query = db.collection(collection_name)


query_watch = collection_query.on_snapshot(on_snapshot)

#if you log new data, you have to rerun the command below to see the data in your dataframe (while it will be already in the firestore collection
df_raw = pd.DataFrame(CreateTable(['userId', 'data', 'date', 'type', 'currentView', 'item'], firestore_collection))

#examples of filtering
df_csv= df_raw.loc[(df_raw.date>="2021-01-07")&(df_raw.item=='Challenge')].sort_values(by='date')

#example of exporting
df_csv.to_csv("data/df_csv.csv", index=False)