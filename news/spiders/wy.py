import json
from typing import Iterable

import requests
import scrapy
from ..items import NewsItem
from scrapy import Request


class WySpider(scrapy.Spider):
    name = "wy"
    allowed_domains = ["news.163.com"]
    start_urls = ["https://news.163.com"]

    def start_requests(self) -> Iterable[Request]:
        yield Request(url=self.start_urls[0], callback=self.parse_start)

    def parse_start(self, response):
        urls = {'国内': 'cm_guonei', '国际': 'cm_guoji', '军事': 'cm_war', '航空': 'cm_hangkong'}
        for tag, url in urls.items():
            index_url = f'https://news.163.com/special/{url}/?callback=data_callback'
            yield Request(url=index_url, callback=self.parse_index, dont_filter=True, meta={'type': tag})

    def parse_index(self, response):
        article_type = response.meta['type']
        article_urls = json.loads(response.text[14:-1])
        for article_url in article_urls:
            item = NewsItem()
            url = article_url['docurl']
            api = url[-21:-5]
            item = self.get_amt(api, item)

            item['type'] = article_type

            keywords = article_url['keywords']
            item['keywords'] = self.get_keyword(keywords)
            yield Request(url=url, callback=self.parse, dont_filter=True, meta={'item': item})

    # 爬取关键词
    def get_keyword(self, keywords):
        if keywords:
            keyword = [key['keyname'] for key in keywords]
            return '/'.join(keyword)
        else:
            return '空'

    # 评论人数与参与人数
    def get_amt(self, api, item):
        url = f'https://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{api}?ibc=jssdk'
        response = requests.get(url)
        dicts = response.json()
        item['cmtCount'] = dicts.get('cmtCount')
        item['tcount'] = dicts.get('tcount')
        return item

    # 详细信息爬取
    def parse(self, response, **kwargs):
        item = response.meta['item']
        title = response.css('.post_main h1::text').get()
        item['title'] = title
        print(f'爬取: {title}中， url：{response.url}')
        post_info = response.css('.post_info::text').getall()
        time_addr = ''.join(post_info).replace('\n', '')

        time, addr = time_addr.split('　来源:')
        item['time'] = time.strip()
        item['address'] = addr.strip()
        source = response.css('.post_info a::text').get()
        item['source'] = source
        content = response.css('.post_body p::text').extract()
        con = ''.join([i.replace('\n', '').strip() for i in content])
        item['content'] = con
        yield item
