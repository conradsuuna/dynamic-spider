# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyfarmspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    internal_url = scrapy.Field()
    all_data = scrapy.Field()

class CropSpiderItem(scrapy.Item):
    name = scrapy.Field()
    email = scrapy.Field()

'''class Diseases(scrapy.Item):
    name = scrapy.Field()

class getInternalLinks(scrapy.Item):
    

class getAllData(scrapy.Item):
    all_data = scrapy.Field()'''
