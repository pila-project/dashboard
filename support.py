import pandas as pd

def DfReader(filename, extension, subdir=''):
    '''currently supports csv, txt, xlsx, json list
    add sql
    control column names'''
    if len(subdir) > 0:
        subdir += "/"

    if extension == 'csv':

        filepath = "{}{}.".format(subdir,filename)
        df = pd.read_table(filepath,sep=',')