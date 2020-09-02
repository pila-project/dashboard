from google.cloud import firestore
import pandas as pd
import threading


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
        key_name: str,
        dict_name: str
):
    table = []
    # add sorting by timestamp
    [table.append(ev.get(key_name)) for ev in dict_name]

    return table



