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
    categories = scrapy.Field()
    socials = scrapy.Field()
    rating = scrapy.Field()
    about = scrapy.Field()
    team = scrapy.Field()
    advisors = scrapy.Field()
    advisor = scrapy.Field()

class PersonItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    links = scrapy.Field()
    source_page_url = scrapy.Field()

class FinanceItem(scrapy.Item):
    _id = scrapy.Field()
    token = scrapy.Field()
    type = scrapy.Field()
    price_preico = scrapy.Field()
    price = scrapy.Field()
    bonus = scrapy.Field()
    bounty = scrapy.Field()
    mvp_prototype = scrapy.Field()
    platform = scrapy.Field()
    accepting = scrapy.Field()
    min_invest = scrapy.Field()
    hard_cap = scrapy.Field()
    country = scrapy.Field()
    kyc = scrapy.Field()

