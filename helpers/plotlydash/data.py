"""Prepare data for Plotly Dash."""
import pandas as pd
import numpy as np

from .filemanager import ReadFirestoreCollection, TimeConverter, CreateTable, FirestoreListener
from collections import Counter
from google.cloud import firestore


# def create_dataframe():
#     """Create Pandas DataFrame from local CSV."""
#     df = pd.read_csv('data/311-calls.csv', parse_dates=['created'])
#     df['created'] = df['created'].dt.date
#     df.drop(columns=['incident_zip'], inplace=True)
#     num_complaints = df['complaint_type'].value_counts()
#     to_remove = num_complaints[num_complaints <= 30].index
#     df.replace(to_remove, np.nan, inplace=True)
#     return df




def CreateDataFrame(collection_name:str="karelDB"):


    results =  ReadFirestoreCollection(collection_name=collection_name) #ReadFirestoreCollection(collection_name=collection_name)

    counter = Counter(CreateTable('data',results))

    df = pd.DataFrame(list(counter.items()),columns = ['Action','Count'])

    return df


# def CreateDataTable(collection_name="karelDB"):
#
#     df=pd.DataFrame{'Action': {0: 'Welcome',
#                 1: 'MeetKarel',
#                 2: 'KarelCommandsMove',
#                 3: 'KarelCommandsTurnLeft',
#                 4: 'KarelCommandsPickStone',
#                 5: 'KarelCommandsPlaceStone'},
#      'Count': {0: 3, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}}
#
#     return df