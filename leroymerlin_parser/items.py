# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
import re

def prices_to_int(value):
    if value:
        return int(re.sub("\D", "", value))

class LeroyMerlinParserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(prices_to_int))
    characteristics = scrapy.Field()
    characteristics_term = scrapy.Field()
    characteristics_def = scrapy.Field()
    link = scrapy.Field()
    pass
