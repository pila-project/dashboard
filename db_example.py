from google.cloud import firestore
import pandas as pd


def ReadFirestoreCollection(collection_name: str = "karelDB"):

    db = firestore.Client.from_service_account_json("keys/pila-277913-44ed571ccec0.json")

    firestore_collection = []
    [firestore_collection.append(dic.to_dict()) for dic in db.collection(collection_name).stream()]

    return firestore_collection


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


results = ReadFirestoreCollection(collection_name='karelDB')

#if you log new data, you have to rerun the command below to see the data in your dataframe (while it will be already in the firestore collection
df_raw = pd.DataFrame(CreateTable(['userId', 'data', 'date', 'type', 'currentView', 'item'], results))

#examples of filtering
# print(df_raw.date.dtype)
df_csv= df_raw.loc[(df_raw.date>='2021-01-08')].sort_values(by='date')
# print(df_csv)
# #example of exporting
df_csv.to_csv("data/df_csv2.csv", index=False)