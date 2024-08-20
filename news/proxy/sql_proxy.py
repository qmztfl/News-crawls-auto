# import mysql.connector
# from mysql.connector import Error
from pymysql import connect, Error

"""
数据处理文件
"""


class sql_proxy:

    def __init__(self, host='localhost',
                 database='proxy',
                 user='root',
                 password='26938'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connect = self.__connect_to_database(self.host, self.database, self.user, self.password)
        self.create_table()

    def __connect_to_database(self, host, database, user, password):
        try:
            connection = connect(host=host,
                                 database=database,
                                 user=user,
                                 password=password)
            if connection:
                # print("连接成功！")
                return connection
        except Error as e:
            print("连接失败：", e)
        return None

    def read_proxy(self):
        connection = self.connect
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT addr FROM proxy where num=100 ORDER BY RAND() LIMIT 1")
            result = cursor.fetchone()[0]
            return result
        except Exception as e:
            print(f'错误: {e}')

    def read_proxys(self):
        connection = self.connect
        try:
            # 使用 cursor() 方法创建一个游标对象
            cursor = connection.cursor()
            cursor.execute("SELECT addr FROM proxy")
            result = cursor.fetchall()
            result = [i[0] for i in result]
            return result
        finally:
            # 关闭数据库连接
            # connection.close()
            print('完成表批量查找操作！')

    def create_table(self):
        create_table_query = """
                        CREATE TABLE IF NOT EXISTS `proxy` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `addr` varchar(255) DEFAULT NULL,
                        `num` int(11) DEFAULT NULL,
                        PRIMARY KEY (`id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
                        """
        connection = self.connect
        cursor = connection.cursor()
        try:
            cursor.execute(create_table_query)
            # print("表创建成功！")
        except Error as e:
            print("表创建失败：", e)

    def proxyIpstore(self, good_ips):
        """
        插入代理地址
        :param good_ips: 代理地址列表
        :return:
        """
        insert_data_query = """
                INSERT INTO proxy(addr, num) VALUES (%s,%s)
                """
        # 连接数据库
        connection = self.connect
        if connection:
            # 插入数据
            data = []
            for i in good_ips:
                data.append((i, 90))
            cursor = connection.cursor()
            try:
                cursor.executemany(insert_data_query, data)
                connection.commit()
                # cursor.execute(insert_data_query, data)
            finally:
                print('完成表插入操作！')
                # 去除重复代理
                self.updata("DELETE t1 FROM proxy t1 INNER JOIN proxy t2 WHERE t1.id > t2.id AND t1.addr=t2.addr")

    def updata(self, sql_update):
        # sql_update = f"update  proxy  set num=num-5  where  addr='{proxyip}'"
        cursor = self.connect.cursor()
        try:
            cursor.execute(sql_update)
            self.connect.commit()
        except Error as e:
            print("修改失败：", e)
        finally:
            # cursor.close()
            print('完成表更新操作！')

    def del_proxy(self):
        sql = 'DELETE FROM proxy  WHERE num = 0'
        cursor = self.connect.cursor()
        try:
            cursor.execute(sql)
            self.connect.commit()
        except Error as e:
            print("删除失败：", e)
        finally:
            # cursor.close()
            print('完成表删除操作！')
