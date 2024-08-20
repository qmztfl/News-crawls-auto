import pandas as pd
import pymysql
from .line import line
from .bar import bar
from .word import word_clouds
from .map import map
from .table import table


class data:
    def __init__(self):
        self.con = self.dbHandle()
        self.df = self.get_sql()

    def dbHandle(self):
        conn = pymysql.connect(
            host="localhost",
            user="root",
            passwd="26938",
            database='proxy',
        )
        return conn

    def get_sql(self):
        sql = "SELECT id, title,time,source,address, type, keywords, tcount, cmtCount FROM articles"
        df = pd.read_sql(sql, self.con, index_col='id')
        return df

    def index(self):
        index = dict()
        line_data = line(self.df)

        bar_data = bar(self.df)
        index['line'] = line_data
        index['bar'] = bar_data

        index['word_clouds'] = word_clouds(self.df)
        index['map'] = map(self.df)
        index['table'] = table(self.df)
        return index

    def guoji(self):
        df = self.df[self.df['type'] == '国际']
        index = dict()
        line_data = line(df)

        bar_data = bar(df)
        index['line'] = line_data
        index['bar'] = bar_data

        index['word_clouds'] = word_clouds(df)
        return index

    def guonei(self):
        df = self.df[self.df['type'] == '国内']
        index = dict()
        line_data = line(df)

        bar_data = bar(df)
        index['line'] = line_data
        index['bar'] = bar_data

        index['word_clouds'] = word_clouds(df)
        return index

    def war(self):
        df = self.df[self.df['type'] == '军事']
        index = dict()
        line_data = line(df)

        bar_data = bar(df)
        index['line'] = line_data
        index['bar'] = bar_data

        index['word_clouds'] = word_clouds(df)
        return index

    def hangkong(self):
        df = self.df[self.df['type'] == '航空']
        index = dict()
        line_data = line(df)

        bar_data = bar(df)
        index['line'] = line_data
        index['bar'] = bar_data

        index['word_clouds'] = word_clouds(df)
        return index


if __name__ == "__main__":
    a = data()
    a.index()
