# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IcoParserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    slogan = scrapy.Field()
    description = scrapy.Field()
    tags = scrapy.Field()
    links = scrapy.Field()
    rating = scrapy.Field()
    about = scrapy.Field()
    team = scrapy.Field()
    advisers = scrapy.Field()
    whitepaper_file_url = scrapy.Field()
    whitepaper_file = scrapy.Field() 

class PersonItem(scrapy.Item):
    _id = scrapy.Field()
    url_id = scrapy.Field()
    name = scrapy.Field()
    social_links = scrapy.Field()
