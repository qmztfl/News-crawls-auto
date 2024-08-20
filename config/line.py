# '2024-06-18 15:57:21'
import pandas as pd


def line(df: pd.DataFrame):
    df.loc[:, 'time'] = df['time'].str[:10]
    counts = df['time'].value_counts().sort_index()
    date = counts.index.tolist()
    count = counts.values.tolist()
    return {'labels': date, 'series': count}
