import requests
import random
from bs4 import BeautifulSoup
"""
数据爬取文件
"""

urls = [
        "http://www.ip3366.net/free/?stype=1&page={page}",
        "https://www.89ip.cn/index_{page}.html"
    ]

def get_proxys(pages):
    # 定义proxy_ips列表存储代理地址
    proxy_ips = set()
    # 设置headers
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    ]
    ua = uas[random.randint(0, len(uas) - 1)]

    headers = {"User-Agent": ua}
               # 'Cookie': 'https_waf_cookie=ddef8254-fef6-4cb8120647bf9139a546756c6fb4c1471692; Hm_lvt_f9e56acddd5155c92b9b5499ff966848=1716781023,1716950935; Hm_lpvt_f9e56acddd5155c92b9b5499ff966848=1716950935'}
    # 从第一页开始循环访问
    for page in range(1, pages):
        print(f"正在爬取第{page}页!")
        url = f"https://www.89ip.cn/index_{page}"

        res = requests.get(url=url, headers=headers)
        print(res.status_code)
        # 使用.text属性获取网页内容，赋值给html
        html = res.text
        # 用BeautifulSoup()传入变量html和解析器lxml，赋值给soup
        soup = BeautifulSoup(html, "lxml")
        # 使用find_all()方法查找类名为layui-table的标签

        table = soup.find_all(class_="layui-table")[0]
        # 使用find_all()方法查找tr标签
        trs = table.find_all("tr")
        # 使用for循环逐个访问trs列表中的tr标签,一个tr代表一行，第一行为表头，不记录
        for i in range(1, len(trs)):
            # 使用find_all()方法查找td标签
            ip = trs[i].find_all("td")[0].text.strip()
            port = trs[i].find_all("td")[1].text.strip()
            # 拼接代理地址
            proxy_ip = f"http://{ip}:{port}"
            # 将获取的代理地址保存到proxy_ips列表
            proxy_ips.add(proxy_ip)
    return proxy_ips
