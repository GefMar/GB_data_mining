# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IcoParserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    slogan = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    official_link = scrapy.Field()
    project_social_links = scrapy.Field()
    ratings = scrapy.Field()
    experts_ratings = scrapy.Field()
    about = scrapy.Field()
    team = scrapy.Field()
    advisors = scrapy.Field()
    preico_time = scrapy.Field()
    ico_time = scrapy.Field()
    status = scrapy.Field()
    token = scrapy.Field()
    type = scrapy.Field()
    preico_price = scrapy.Field()
    price = scrapy.Field()
    bonus = scrapy.Field()
    bounty = scrapy.Field()
    mvp_prototype = scrapy.Field()
    platform = scrapy.Field()
    accepting = scrapy.Field()
    minimum_investment = scrapy.Field()
    soft_cap = scrapy.Field()
    hard_cap = scrapy.Field()
    country = scrapy.Field()
    whitelist_kyc = scrapy.Field()
    restricted_areas = scrapy.Field()
    price_in_ico = scrapy.Field()
    ico_start = scrapy.Field()
    ico_end = scrapy.Field()


class PersonItem(scrapy.Item):
    _id = scrapy.Field()
    person_url = scrapy.Field()
    name = scrapy.Field()
    social_links = scrapy.Field()


class IcoRatingItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    project_links = scrapy.Field()
    investment_rating = scrapy.Field()
    hype_score = scrapy.Field()
    risk_score = scrapy.Field()
    team = scrapy.Field()
    advisors = scrapy.Field()
