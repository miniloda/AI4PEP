import pandas as pd
import os


def load_data():
    data = pd.read_csv("../NER/data/ILI_estimate.csv")
    return data

def filter_data(data):
    data['Date of Encounter'] = pd.to_datetime(data['Date of Encounter'])
    data['Date of Encounter'] = data['Date of Encounter'].dt.strftime('%Y-%m-%d')
    filtered_data = data["Date of Encounter"].value_counts().sort_index()
    filtered_data.columns = ['dates', 'count']
    return filtered_data
