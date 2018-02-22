# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TktdttItem(scrapy.Item):
    job = scrapy.Field()
    company = scrapy.Field()
    require = scrapy.Field()
    # salary = scrapy.Field()
    # exp = scrapy.Field()
    # quantum = scrapy.Field()
    # description = scrapy.Field()
    # benefit = scrapy.Field()
    # require = scrapy.Field()
    # cv = scrapy.Field()
    # addresscompany = scrapy.Field()
    # deadline = scrapy.Field()
    # skill = scrapy.Field()
