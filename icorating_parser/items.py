# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IcoratingParserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    area = scrapy.Field()
    overview = scrapy.Field()
    feats = scrapy.Field()
    start_ico = scrapy.Field()
    end_ico = scrapy.Field()
    invest_rating = scrapy.Field()
    hype_score = scrapy.Field()
    risk_score = scrapy.Field()
    links = scrapy.Field()
    team_members = scrapy.Field()
    advisors = scrapy.Field()
