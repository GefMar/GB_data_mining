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
    # profile_rating = scrapy.Field()
    experts_ratings = scrapy.Field()
    about = scrapy.Field()
    team = scrapy.Field()
    advisors = scrapy.Field()


class PersonItem(scrapy.Item):
    _id = scrapy.Field()
    person_url = scrapy.Field()
    name = scrapy.Field()
    social_links = scrapy.Field()
