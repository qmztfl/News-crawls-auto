import subprocess
import time
from datetime import datetime

from scrapy import cmdline

from news.proxy.get_proxy import get_proxys
from news.proxy.sql_proxy import sql_proxy
from news.proxy.test_proxy import test_proxy
import json


def update_proxy():
    sql = sql_proxy()
    lists = sql.read_proxys()
    for index, proxy in enumerate(lists):
        # if index == 10:
        #     break
        test_proxy(proxy)
    sql.del_proxy()


def crawl_proxy():
    sql = sql_proxy()
    # 获取代理
    proxys = get_proxys(4)
    # 存储代理
    sql.proxyIpstore(proxys)

    # lists = pro.read_proxys()
    # for i in lists:
    #     test_proxy(i)


def main_proxy():
    with open('package.json', 'r') as fp:
        data = json.load(fp)
    now_time = datetime.now()
    update_time = datetime.strptime(data['time']['update'], "%Y%m%d%H%M%S")
    crawl_time = datetime.strptime(data['time']['crawl'], "%Y%m%d%H%M%S")

    if (now_time - update_time).total_seconds() > data['interval']['update']:
        print('更新代理中...')
        update_proxy()
        data['time']['update'] = time.strftime("%Y%m%d%H%M%S", time.localtime())
        print('更新代理完成！')

    if (now_time - crawl_time).total_seconds() > data['interval']['crawl']:
        print('爬取代理中...')
        data['time']['crawl'] = time.strftime("%Y%m%d%H%M%S", time.localtime())
        crawl_proxy()
        print('爬取代理完成！')

    data['time']['update'] = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # dt_object = datetime.strptime(data['time']['update'], "%Y%m%d%H%M%S")
    with open('package.json', 'w') as fp:
        fp.write(json.dumps(data))


def get_data():
    with open('package.json', 'r') as fp:
        data = json.load(fp)
    now_time = datetime.now()
    crawl_time = datetime.strptime(data['time']['getdata'], "%Y%m%d%H%M%S")
    print(now_time)
    if (now_time - crawl_time).total_seconds() > data['interval']['getdata']:
        print('爬取数据中...')
        # subprocess.run(['scrapy', 'crawl', 'wy', '-o', 'data.json'])
        subprocess.run(['scrapy', 'crawl', 'wy'])
        data['time']['getdata'] = time.strftime("%Y%m%d%H%M%S", time.localtime())
        print('爬取数据完成！')
    # data['time']['getdata'] = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # dt_object = datetime.strptime(data['time']['update'], "%Y%m%d%H%M%S")
    with open('package.json', 'w') as fp:
        fp.write(json.dumps(data))


def scrapy_main():
    # main_proxy()
    while True:
        get_data()
        time.sleep(60)


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # cmdline.execute("scrapy crawl wy".split())
    cmdline.execute("scrapy crawl wy -o data.json".split())
