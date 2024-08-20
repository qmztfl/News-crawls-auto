# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NewsPipeline:
    def process_item(self, item, spider):
        return item


import pymysql


# 连接数据库
def dbHandle():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd="26938",
        database='proxy',
    )
    return conn


def create_table(conn):
    mycursor = conn.cursor()
    # SQL 创建表语句
    sql = '''  
    CREATE TABLE IF NOT EXISTS articles (  
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,  
        time VARCHAR(255) NOT NULL,
        source VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL,
        content longtext NOT NULL,
        type VARCHAR(255) NOT NULL,
        keywords VARCHAR(255) NOT NULL,
        tcount VARCHAR(255) NOT NULL,
        cmtCount VARCHAR(255) NOT NULL
    )  
    '''
    try:
        # 执行SQL语句
        mycursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
    except pymysql.Error as e:
        print("创建表错误！错误在这里>>>>>>>", e, "<<<<<<<错误在这里")


class sqlSpiderPipeline:
    """
    数据持久化
    """
    def __init__(self):
        self.dbObject = dbHandle()
        self.cursor = self.dbObject.cursor()
        create_table(self.dbObject)

    def repeat(self, title) -> bool:
        """
        有重复返回真
        :param title:
        :return:
        """
        try:
            query = "SELECT * FROM articles WHERE title=%s"
            self.cursor.execute(query, (title,))
            result = self.cursor.fetchall()
            return True if result else False
        except BaseException as e:
            print("错误在这里>>>>>>>", e, "<<<<<<<错误在这里")
            return True

    def process_item(self, item, spider):
        # 插入数据库
        sql = "INSERT INTO articles(title,time,source,address,content, type, keywords, tcount, cmtCount) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        if self.repeat(item['title']):
            self.updata_item(item)
            return item
        try:
            self.cursor.execute(sql,
                                (item['title'], item['time'], item['source'], item['address'], item['content'], item['type'], item['keywords'], item['tcount'], item['cmtCount']))
            self.cursor.connection.commit()
            print('插入数据：《', item['title'], "》", item['time'], item['source'], item['address'], item['content'], item['type'], item['keywords'], item['tcount'], item['cmtCount'])
        except BaseException as e:
            print("错误在这里>>>>>>>", e, "<<<<<<<错误在这里")
            self.dbObject.rollback()
        return item

    def updata_item(self, item):
        # 更新数据库
        sql = "UPDATE articles SET tcount = %s, cmtCount = %s WHERE title = %s"
        try:
            self.cursor.execute(sql,
                                (item['tcount'], item['cmtCount'], item['title'] ))
            self.cursor.connection.commit()
            print('更新数据：', item['title'], item['tcount'], item['cmtCount'])
        except BaseException as e:
            print("错误在这里>>>>>>>", e, "<<<<<<<错误在这里")
            self.dbObject.rollback()
        return item
