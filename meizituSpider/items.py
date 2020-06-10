# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MeizituspiderItem(scrapy.Item):  # pylint: disable=too-many-ancestors
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    imgs = scrapy.Field()
    date = scrapy.Field()
