import pandas as pd


def pie(df: pd.DataFrame):
    n = 9
    counts = df['source'].value_counts()
    date = counts.index.tolist()
    count = counts.values.tolist()
    if len(date) > n and len(count) > n:
        date = date[:n]
        date.append('其他')
        sun = sum(count[n + 1:])
        count = count[:n]
        count.append(sun)
    return {'labels': date, 'series': count}
