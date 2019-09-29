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
    rating_list = scrapy.Field()
    about = scrapy.Field()
    team = scrapy.Field()
    advisers = scrapy.Field()
    preico_time = scrapy.Field()
    ico_time = scrapy.Field()
    token = scrapy.Field()
    preico_price = scrapy.Field()
    price = scrapy.Field()
    bonus = scrapy.Field()
    platform = scrapy.Field()
    investment = scrapy.Field()
    soft_cap = scrapy.Field()
    hard_cap = scrapy.Field()
    country = scrapy.Field()
    whitelist_KYC = scrapy.Field()
    country = scrapy.Field()
    restricted_areas = scrapy.Field()

class PersonItem(scrapy.Item):
    _id = scrapy.Field()
    url_id = scrapy.Field()
    name = scrapy.Field()
    social_links = scrapy.Field()

class IcoRatingItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    links = scrapy.Field()
    investment_rating = scrapy.Field()
    hype_score = scrapy.Field()
    risk_score = scrapy.Field()
    team = scrapy.Field()
    advisers = scrapy.Field()
    ico_time_start = scrapy.Field()
    ico_time_end = scrapy.Field()