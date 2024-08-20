# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    address = scrapy.Field()
    content = scrapy.Field()
    type = scrapy.Field()
    keywords = scrapy.Field()
    cmtCount = scrapy.Field()
    tcount = scrapy.Field()
