# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WpaperItem(scrapy.Item):
    img_true = scrapy.Field()
    img_small = scrapy.Field()
    Avatar = scrapy.Field()
    Uploader = scrapy.Field()
    Category = scrapy.Field()
    Resolution = scrapy.Field()
    Contrast = scrapy.Field()
    Size = scrapy.Field()
    Tags = scrapy.Field()