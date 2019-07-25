# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, TakeFirst


class IcoParserItem(scrapy.Item):
    name = scrapy.Field()
    slogan = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    site = scrapy.Field()
    socials = scrapy.Field()
    ratings = scrapy.Field()
    about_section = scrapy.Field()
    team = scrapy.Field()
    whitepaper = scrapy.Field()
    stored_whitepaper = scrapy.Field()


class IcoParserItemLoader(ItemLoader):
    name_out = TakeFirst()
    slogan_out = TakeFirst()
    description_out = TakeFirst()
    categories_out = Identity()
    site_out = TakeFirst()
    socials_out = Identity()
    ratings_out = TakeFirst()
    about_section_in = Join('')
    about_section_out = TakeFirst()
    team_out = TakeFirst()
    whitepaper_out = Identity()


class Person(scrapy.Item):
    profile = scrapy.Field()
    name = scrapy.Field()
    job = scrapy.Field()
    socials = scrapy.Field()


class PersonLoader(ItemLoader):
    profile_out = TakeFirst()
    name_out = TakeFirst()
    job_out = TakeFirst()
    socials_out = Identity()