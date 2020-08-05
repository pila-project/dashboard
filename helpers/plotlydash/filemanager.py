from google.cloud import firestore
import pandas as pd



def ReadFirestoreDocument(doc_name: str, db_name: str = "karelDB"):
    db = firestore.Client.from_service_account_json("keys/pila-277913-44ed571ccec0.json")

    doc_ref = db.collection(db_name).document(doc_name)

    doc = doc_ref.get()

    return doc.to_dict()


def ReadFirestoreCollection(db_name: str = "karelDB"):

    db = firestore.Client.from_service_account_json("keys/pila-277913-44ed571ccec0.json")

    print(db.project, db.SCOPE)

    firestore_collection = []
    [firestore_collection.append(dic.to_dict()) for dic in db.collection(db_name).stream()]

    return firestore_collection



def TimeConverter(timecol, fmt="%Y-%m-%dT%H:%M:%S.%fZ"):
    '''Converts time feature to a given format'''
    return pd.to_datetime(timecol, format=fmt)


def CreateTable(key_name: str, dict_name: str):
    table = []
    # sort by timestamp
    [table.append(ev.get(key_name)) for ev in dict_name]

    return table