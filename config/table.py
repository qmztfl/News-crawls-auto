import pandas as pd


def table(df: pd.DataFrame):
    dicts = df.to_dict(orient='records')
    return dicts
