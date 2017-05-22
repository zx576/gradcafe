# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GradcafeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    institution = scrapy.Field()
    program = scrapy.Field()
    decision = scrapy.Field()
    date = scrapy.Field()
    st = scrapy.Field()
    date_added = scrapy.Field()
    notes = scrapy.Field()
    page_count = scrapy.Field()
