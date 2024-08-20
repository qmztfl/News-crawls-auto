import pandas as pd


def word_clouds(df: pd.DataFrame):
    dp = df[df['keywords'] != '空']
    dp = dp['keywords'].tolist()
    keywords = '/'.join(dp)
    fp = {'keywords': keywords.split('/')}
    fp = pd.DataFrame(fp)

    counts = fp['keywords'].value_counts()
    # date = counts.index.tolist()
    # count = counts.values.tolist()
    data = list(zip(counts.index.tolist(), counts.values.tolist()))
    word = [{'name': i, 'value': j} for i, j in data]
    return word
