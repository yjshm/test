# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YoupornItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # item 
    class1 = scrapy.Field()
    class2 = scrapy.Field()
    class3 = scrapy.Field()
    title  = scrapy.Field()
    link   = scrapy.Field()
    description = scrapy.Field()
    guid        = scrapy.Field()
    pubDate     = scrapy.Field()
    
    #category = scrapy.Field()
    