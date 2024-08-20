from .sql_proxy import sql_proxy
from .get_proxy import get_proxys
import requests
import time

import random

"""
数据检测文件
"""

uas = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"]


def test_proxy(proxyips):
    # url = "http://httpbin.org/ip"
    url = "http://icanhazip.com"
    proxy_ip = {"http": proxyips}
    print(proxy_ip)
    # 设置代理信息
    # 从uas列表中随取一个ua作为User-Agent
    ua = uas[random.randint(0, len(uas) - 1)]
    # 设置headers
    headers = {
        "User-Agent": ua
    }
    sql = sql_proxy()
    try:
        res = requests.get(url, headers=headers, proxies=proxy_ip, timeout=30)
        if res.status_code == 200:
            # 访问成功
            print(f"访问成功，状态：{res.status_code}, proxy_ip: {proxyips},url: {url}")
            # 将这条代理数据的num修改为100
            sql_update = "update  proxy  set num=100  where  addr='" + proxyips + "'"
            sql.updata(sql_update)
        else:
            sql_update = "update  proxy  set num=num-10  where  addr='" + proxyips + "'"
            sql.updata(sql_update)
            print(f"访问失败,状态：{res.status_code}, proxy_ip:{proxy_ip},url: {url}")
    except requests.exceptions.RequestException as e:
        # 访问失败
        # 修改不能使用的代理num值
        sql_update = "update  proxy  set num=num-10  where  addr='" + proxyips + "'"
        sql.updata(sql_update)
        print(f"访问失败, proxy_ip:{proxy_ip},url: {url}")
        print(f'错误：{e}')
    # else:

    # html = res.text
    finally:
        time.sleep(2)
    print(f"代理池数据存储成功\n")


if __name__ == '__main__':
    pro = sql_proxy()
    # 获取代理
    proxys = get_proxys(2)
    # 存储代理
    pro.proxyIpstore(proxys)

