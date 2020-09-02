"""Prepare data for Plotly Dash."""
import pandas as pd
import numpy as np

from .filemanager import ReadFirestoreCollection, TimeConverter, CreateTable, FirestoreListener
from collections import Counter
from google.cloud import firestore



def CreateDataFrame(collection_name:str="karelDB"):
    results = FirestoreListener(collection_name=collection_name)
    print(results)

    counter = Counter(CreateTable('data', results))

    df = pd.DataFrame(list(counter.items()), columns=['Action', 'Count'])

    return df


# def CreateDataFrame(collection_name="karelDB"):
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