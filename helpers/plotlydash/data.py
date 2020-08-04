"""Prepare data for Plotly Dash."""
import pandas as pd
import numpy as np

# def create_dataframe():
#     """Create Pandas DataFrame from local CSV."""
#     df = pd.read_csv('data/311-calls.csv', parse_dates=['created'])
#     df['created'] = df['created'].dt.date
#     df.drop(columns=['incident_zip'], inplace=True)
#     num_complaints = df['complaint_type'].value_counts()
#     to_remove = num_complaints[num_complaints <= 30].index
#     df.replace(to_remove, np.nan, inplace=True)
#     return df


from .filemanager import ReadFirestoreCollection, TimeConverter, CreateTable
from collections import Counter


def CreateDataTable(db_name:str="karelDB"):

    results =  ReadFirestoreCollection(db_name=db_name)

    counter = Counter(CreateTable('data',results))

    df = pd.DataFrame(list(counter.items()),columns = ['Action','Count'])

    return df